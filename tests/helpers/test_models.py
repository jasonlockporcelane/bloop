import bloop.condition
from bloop import (
    new_base, Column, DateTime, Float, GlobalSecondaryIndex,
    Integer, List, LocalSecondaryIndex, Map, String, UUID)

DocumentType = Map(**{
    'Rating': Float(),
    'Stock': Integer(),
    'Description': Map(**{
        'Heading': String,
        'Body': String,
        'Specifications': String
    }),
    'Id': UUID,
    'Updated': DateTime
})
BaseModel = new_base()


class Document(BaseModel):
    id = Column(Integer, hash_key=True)
    data = Column(DocumentType)
    numbers = Column(List(Integer))


class User(BaseModel):
    id = Column(UUID, hash_key=True)
    age = Column(Integer)
    name = Column(String)
    email = Column(String)
    joined = Column(DateTime, name="j")
    by_email = GlobalSecondaryIndex(
        hash_key="email", projection="all")


class SimpleModel(BaseModel):
    class Meta:
        table_name = "Simple"
    id = bloop.Column(bloop.String, hash_key=True)


class ComplexModel(BaseModel):
    class Meta:
        write_units = 2
        read_units = 3
        table_name = "CustomTableName"

    name = Column(UUID, hash_key=True)
    date = Column(String, range_key=True)
    email = Column(String)
    joined = Column(String)
    not_projected = Column(Integer)
    by_email = GlobalSecondaryIndex(
        hash_key="email", read_units=4, projection="all", write_units=5)
    by_joined = LocalSecondaryIndex(
        range_key="joined", projection=["email"])

conditions = set()


def _build_conditions():
    """This is a method so that we can name each condition before adding it.

    This makes the conditions self-documenting;
    simplifies building compound conditions;
    eases extension for new test cases
    """
    empty = bloop.condition.Condition()
    lt = Document.id < 10
    gt = Document.id > 12

    path = Document.data["Rating"] == 3.4

    # Order doesn't matter for multi conditions
    basic_and = lt & gt
    swapped_and = gt & lt
    multiple_and = lt & lt & gt

    basic_or = lt | gt
    swapped_or = gt | lt
    multiple_or = lt | lt | gt

    not_lt = ~lt
    not_gt = ~gt

    not_exists_data = Document.data.is_(None)
    not_exists_id = Document.id.is_(None)
    exists_id = Document.id.is_not(None)

    begins_hello = Document.id.begins_with("hello")
    begins_world = Document.id.begins_with("world")
    begins_numbers = Document.numbers.begins_with(8)

    contains_hello = Document.id.contains("hello")
    contains_world = Document.id.contains("world")
    contains_numbers = Document.numbers.contains(9)

    between_small = Document.id.between(5, 6)
    between_big = Document.id.between(100, 200)
    between_numbers = Document.numbers.between(set([8080]), set([8088]))

    in_small = Document.id.in_([3, 7, 11])
    in_big = Document.id.in_([123, 456])
    in_numbers = Document.numbers.in_([120, 450])

    conditions.update((
        empty,
        lt, gt, path,
        basic_and, swapped_and, multiple_and,
        basic_or, swapped_or, multiple_or,
        not_lt, not_gt,
        not_exists_data, not_exists_id, exists_id,
        begins_hello, begins_world, begins_numbers,
        contains_hello, contains_world, contains_numbers,
        between_small, between_big, between_numbers,
        in_small, in_big, in_numbers
    ))
_build_conditions()
