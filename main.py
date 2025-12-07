import json
import os

# File where we store all book data
FILENAME = "library_data.json"

def load_data():
    """Load all books from the JSON file"""
    if os.path.exists(FILENAME):
        with open(FILENAME, 'r') as file:
            return json.load(file)
    return []

def save_data(books):
    """Save all books to the JSON file"""
    with open(FILENAME, 'w') as file:
        json.dump(books, file, indent=4)

def generate_book_id(books):
    """Create a new unique book ID"""
    if len(books) == 0:
        return "BK001"
    
    # Find the highest book ID number and add 1
    highest_id = 0
    for book in books:
        book_number = int(book['book_id'][2:])  # Get number after "BK"
        if book_number > highest_id:
            highest_id = book_number
    
    new_id = highest_id + 1
    return f"BK{new_id:03d}"  # Format as BK001, BK002, etc.

def add_book(books):
    """Add a new book to the library"""
    print("\n--- Add New Book ---")
    title = input("Enter book title: ")
    author = input("Enter author name: ")
    category = input("Enter category: ")
    
    new_book = {
        "book_id": generate_book_id(books),
        "title": title,
        "author": author,
        "category": category,
        "is_available": True,
        "borrower": None
    }
    
    books.append(new_book)
    save_data(books)
    print(f"Book added successfully! Book ID: {new_book['book_id']}")

def delete_book(books):
    """Delete a book from the library"""
    print("\n--- Delete Book ---")
    book_id = input("Enter Book ID to delete: ")
    
    for i in range(len(books)):
        if books[i]['book_id'] == book_id:
            books.pop(i)
            save_data(books)
            print("Book deleted successfully!")
            return
    
    print("Book not found!")

def modify_book(books):
    """Modify details of an existing book"""
    print("\n--- Modify Book ---")
    book_id = input("Enter Book ID to modify: ")
    
    # Find the book
    found_book = None
    for book in books:
        if book['book_id'] == book_id:
            found_book = book
            break
    
    if found_book is None:
        print("Book not found!")
        return
    
    # Show current details
    print("\nCurrent book details:")
    display_book(found_book)
    
    # Get new values
    print("\nEnter new values (press Enter to keep current value):")
    
    new_title = input(f"New Title [{found_book['title']}]: ")
    if new_title:
        found_book['title'] = new_title
    
    new_author = input(f"New Author [{found_book['author']}]: ")
    if new_author:
        found_book['author'] = new_author
    
    new_category = input(f"New Category [{found_book['category']}]: ")
    if new_category:
        found_book['category'] = new_category
    
    save_data(books)
    print("Book modified successfully!")

def search_books(books):
    """Search for books"""
    print("\n--- Search Books ---")
    print("1. Search by Title")
    print("2. Search by Author")
    print("3. Search by Category")
    print("4. Search by Book ID")
    
    search_type = input("\nChoose search type (1-4): ")
    search_query = input("Enter search term: ").lower()
    
    results = []
    
    for book in books:
        if search_type == "1" and search_query in book['title'].lower():
            results.append(book)
        elif search_type == "2" and search_query in book['author'].lower():
            results.append(book)
        elif search_type == "3" and search_query in book['category'].lower():
            results.append(book)
        elif search_type == "4" and search_query in book['book_id'].lower():
            results.append(book)
    
    if len(results) > 0:
        print(f"\nFound {len(results)} book(s):")
        for book in results:
            display_book(book)
    else:
        print("No books found!")

def display_all_books(books):
    """Display all books in the library"""
    print("\n--- All Books in Library ---")
    
    if len(books) == 0:
        print("No books in library!")
        return
    
    for book in books:
        display_book(book)

def display_book(book):
    """Display a single book's details"""
    print("\n" + "="*50)
    print(f"Book ID: {book['book_id']}")
    print(f"Title: {book['title']}")
    print(f"Author: {book['author']}")
    print(f"Category: {book['category']}")
    
    if book['is_available']:
        print("Status: Available")
    else:
        print(f"Status: Borrowed by {book['borrower']}")
    
    print("="*50)

def borrow_book(books):
    """Borrow a book from the library"""
    print("\n--- Borrow Book ---")
    book_id = input("Enter Book ID: ")
    borrower_name = input("Enter your name: ")
    
    for book in books:
        if book['book_id'] == book_id:
            if book['is_available']:
                book['is_available'] = False
                book['borrower'] = borrower_name
                save_data(books)
                print("Book borrowed successfully!")
                return
            else:
                print(f"Book is already borrowed by {book['borrower']}")
                return
    
    print("Book not found!")

def return_book(books):
    """Return a borrowed book"""
    print("\n--- Return Book ---")
    book_id = input("Enter Book ID: ")
    borrower_name = input("Enter your name: ")
    
    for book in books:
        if book['book_id'] == book_id:
            if book['borrower'] and book['borrower'].lower() == borrower_name.lower():
                book['is_available'] = True
                book['borrower'] = None
                save_data(books)
                print("Book returned successfully!")
                return
            else:
                print("This book was not borrowed by you!")
                return
    
    print("Book not found!")

def show_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("LIBRARY MANAGEMENT SYSTEM")
    print("="*50)
    print("1. Add New Book")
    print("2. Delete Book")
    print("3. Modify Book")
    print("4. Search Books")
    print("5. Display All Books")
    print("6. Borrow Book")
    print("7. Return Book")
    print("8. Exit")
    print("="*50)

def main():
    """Main program"""
    books = load_data()
    
    while True:
        show_menu()
        choice = input("\nEnter your choice (1-8): ")
        
        if choice == "1":
            add_book(books)
        elif choice == "2":
            delete_book(books)
        elif choice == "3":
            modify_book(books)
        elif choice == "4":
            search_books(books)
        elif choice == "5":
            display_all_books(books)
        elif choice == "6":
            borrow_book(books)
        elif choice == "7":
            return_book(books)
        elif choice == "8":
            print("\nThank you for using the Library Management System!")
            break
        else:
            print("Invalid choice! Please enter a number between 1-8.")

# Start the program
if __name__ == "__main__":
    main()