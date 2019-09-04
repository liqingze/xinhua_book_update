from common.models.book.BookStockChangeLog import BookStockChangeLog
from common.models.book.Book import Book
from common.libs.Helper import getCurrentDate
from application import db


class BookService():

    @staticmethod
    def setStockChangeLog(book_id=0, quantity=0, note=''):
        if book_id < 1:
            return False

        book_info = Book.query.filter_by(id=book_id).first()
        if not book_info:
            return False

        model_stock_change = BookStockChangeLog()
        model_stock_change.book_id = book_id
        # 变更量
        model_stock_change.unit = quantity
        model_stock_change.total_stock = book_info.stock
        model_stock_change.note = note
        model_stock_change.created_time = getCurrentDate()
        db.session.add(model_stock_change)
        db.session.commit()
        return True
