

const defaultItems = [
    {
        id: 1,
        name: "Black Wireless Headphones",
        category: "Electronics",
        status: "Lost",
        location: "Central Library",
        date: "2026-11-20",
        description: "Black Bluetooth headphones with a charging case.",
        image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600",
        reporter: "Aman",
        email: "aman@example.com"
    },
    {
        id: 2,
        name: "Blue College Backpack",
        category: "Bags",
        status: "Found",
        location: "Main Canteen",
        date: "2026-11-22",
        description: "Blue backpack containing some notebooks.",
        image: "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600",
        reporter: "Priya",
        email: "priya@example.com"
    },
    {
        id: 3,
        name: "Student ID Card",
        category: "Documents",
        status: "Found",
        location: "Computer Lab",
        date: "2026-11-23",
        description: "A university student identity card was found.",
        image: "",
        reporter: "Rahul",
        email: "rahul@example.com"
    },
    {
        id: 4,
        name: "Silver Wrist Watch",
        category: "Accessories",
        status: "Lost",
        location: "Sports Ground",
        date: "2026-11-24",
        description: "Silver-colored wrist watch with a black strap.",
        image: "",
        reporter: "Neha",
        email: "neha@example.com"
    }
];

// Load saved items or show sample items
let items = JSON.parse(localStorage.getItem("campusFindItems"))
    || defaultItems;

const container = document.getElementById("itemsContainer");
const searchInput = document.getElementById("searchInput");
const categoryFilter = document.getElementById("categoryFilter");
const statusFilter = document.getElementById("statusFilter");
const reportForm = document.getElementById("reportForm");

// Save reports in browser storage
function saveItems() {
    localStorage.setItem("campusFindItems", JSON.stringify(items));
}

// Update dashboard statistics
function updateStats() {
    document.getElementById("totalCount").textContent = items.length;

    document.getElementById("lostCount").textContent =
        items.filter(item => item.status === "Lost").length;

    document.getElementById("foundCount").textContent =
        items.filter(item => item.status === "Found").length;

    document.getElementById("returnedCount").textContent =
        items.filter(item => item.status === "Returned").length;
}

// Display item cards
function displayItems() {
    const search = searchInput.value.toLowerCase();
    const category = categoryFilter.value;
    const status = statusFilter.value;

    const filteredItems = items.filter(item => {
        const matchesSearch =
            item.name.toLowerCase().includes(search) ||
            item.location.toLowerCase().includes(search) ||
            item.description.toLowerCase().includes(search);

        const matchesCategory =
            category === "all" || item.category === category;

        const matchesStatus =
            status === "all" || item.status === status;

        return matchesSearch && matchesCategory && matchesStatus;
    });

    container.innerHTML = "";

    document.getElementById("emptyMessage").hidden =
        filteredItems.length !== 0;

    filteredItems.forEach(item => {
        const card = document.createElement("div");
        card.className = "item-card";

        const statusClass =
            item.status === "Found" ? "found" :
            item.status === "Returned" ? "returned" : "";

        // Use a placeholder if no image is supplied
        const image = item.image ||
            "https://placehold.co/600x350/e9effa/2864e8?text=CampusFind+Item";

        // Build card safely using textContent for user data
        const img = document.createElement("img");
        img.className = "item-image";
        img.src = image;
        img.alt = item.name;
        img.onerror = () => {
            img.src = "https://placehold.co/600x350/e9effa/2864e8?text=No+Image";
        };

        const content = document.createElement("div");
        content.className = "item-content";

        const top = document.createElement("div");
        top.className = "item-top";

        const badge = document.createElement("span");
        badge.className = `status ${statusClass}`;
        badge.textContent = item.status;

        const categoryText = document.createElement("small");
        categoryText.textContent = item.category;
        categoryText.style.color = "#77849a";

        top.append(badge, categoryText);

        const title = document.createElement("h3");
        title.textContent = item.name;

        const description = document.createElement("p");
        description.textContent = item.description;

        const location = document.createElement("p");
        location.textContent = "📍 " + item.location;

        const date = document.createElement("p");
        date.textContent = "📅 " + item.date;

        const reporter = document.createElement("p");
        reporter.textContent = "👤 " + item.reporter;

        const contact = document.createElement("a");
        contact.className = "contact-btn";
        contact.textContent = "Contact Reporter";
        contact.href = "mailto:" + item.email;

        content.append(top, title, description, location, date, reporter);

        if (item.status !== "Returned") {
            content.append(contact);

            const returnButton = document.createElement("button");
            returnButton.className = "return-btn";
            returnButton.textContent = "Mark Returned";

            returnButton.addEventListener("click", () => {
                markReturned(item.id);
            });

            content.append(returnButton);
        } else {
            const returnedText = document.createElement("p");
            returnedText.textContent = "✓ Successfully returned";
            returnedText.style.color = "#198653";
            returnedText.style.fontWeight = "bold";
            content.append(returnedText);
        }

        card.append(img, content);
        container.appendChild(card);
    });

    updateStats();
}

// Mark an item as returned
function markReturned(id) {
    const confirmed = confirm(
        "Are you sure this item has been returned?"
    );

    if (!confirmed) return;

    items = items.map(item =>
        item.id === id
            ? { ...item, status: "Returned" }
            : item
    );

    saveItems();
    displayItems();
}

// Submit a new report
reportForm.addEventListener("submit", function(event) {
    event.preventDefault();

    const newItem = {
        id: Date.now(),
        status: document.getElementById("itemStatus").value,
        name: document.getElementById("itemName").value.trim(),
        category: document.getElementById("itemCategory").value,
        location: document.getElementById("itemLocation").value.trim(),
        date: document.getElementById("itemDate").value,
        description: document.getElementById("itemDescription").value.trim(),
        image: document.getElementById("itemImage").value.trim(),
        reporter: document.getElementById("reporterName").value.trim(),
        email: document.getElementById("reporterEmail").value.trim()
    };

    items.unshift(newItem);

    saveItems();

    reportForm.reset();

    document.getElementById("formMessage").textContent =
        "✓ Your report has been submitted successfully!";

    document.getElementById("formMessage").style.color = "green";

    displayItems();

    // Show newly submitted item
    document.getElementById("statusFilter").value = "all";
    document.getElementById("categoryFilter").value = "all";
    document.getElementById("searchInput").value = "";

    displayItems();

    document.getElementById("items").scrollIntoView({
        behavior: "smooth"
    });
});

// Search and filter events
searchInput.addEventListener("input", displayItems);
categoryFilter.addEventListener("change", displayItems);
statusFilter.addEventListener("change", displayItems);

// Set date input maximum to today
document.getElementById("itemDate").max =
    new Date().toISOString().split("T")[0];

// Start the website
displayItems();