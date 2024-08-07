document.addEventListener('DOMContentLoaded', () => {
    const appDiv = document.getElementById('app');
    appDiv.innerHTML = `
        <h2>Welcome to the Bookstore</h2>
        <button id="browseBooks">Browse Books</button>
        <div id="bookList"></div>
    `;

    document.getElementById('browseBooks').addEventListener('click', () => {
        fetch('http://localhost:5000/api/books')  // Change port if different
            .then(response => response.json())
            .then(data => {
                const bookListDiv = document.getElementById('bookList');
                bookListDiv.innerHTML = data.map(book => `
                    <div>
                        <h3>${book.title}</h3>
                        <p>${book.author}</p>
                        <p>Price: ${book.price}</p>
                    </div>
                `).join('');
            });
    });
});
