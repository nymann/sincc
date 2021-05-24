from devtools import debug
from typing import Optional
import pydantic

class Book(pydantic.BaseModel):
    libgen_id: str
    extension: str
    download_url: str
    isbn: str
    year: int
    md5: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    edition: Optional[str] = None
    pages: Optional[str] = None
    filesize: Optional[int] = None

    @classmethod
    def from_libgen_book(cls, book, isbn):
        fields: dict = vars(book)
        year_str: str = fields.pop("year")
        
        if year_str.isdigit():
            year = int(year_str)
        elif ";" in year_str:
            year = int(year_str.split(";").pop())
        else:
            debug(year_str)
            raise ValueError(year_str)
        url = book.get_url()
        fields["libgen_id"] = fields.pop("id")
        return cls(download_url=url, isbn=isbn, year=year, **fields)

    @property
    def filename(self):
        return self.isbn + "." + self.extension
