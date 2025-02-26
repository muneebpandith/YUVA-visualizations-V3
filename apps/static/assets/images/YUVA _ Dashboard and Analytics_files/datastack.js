
        document.addEventListener("DOMContentLoaded", function() {
            fetch("/api/v1/data")  // Update with your actual API endpoint
                .then(response => response.json())
                .then(data => {
                    let datastack = data.datastack;
                    let container = document.getElementById("data-container");
                    container.innerHTML = "";  // Clear existing content

                    Object.keys(datastack).forEach(key => {
                        let dataset = datastack[key];

                        let cardHTML = `
                            <div class="col-md-4 mb-4 d-flex align-items-stretch">
                                <div class="card d-flex flex-column h-100">
                                    <div class="image-container">
                                        <img src="${dataset.thumbnail}" class="card-img-top" alt="Thumbnail">
                                    </div>
                                    <div class="card-body flex-grow-1 d-flex flex-column">
                                        <h5 class="card-title">${dataset.name}</h5>
                                        <p class="card-text">${dataset.basic_info}</p>
                                        <div>
                                            ${dataset.keywords.map(keyword => `<span class="keyword">${keyword}</span>`).join(" ")}
                                        </div>
                                        <a href="/data/${dataset.id}" class="btn btn-primary mt-2">View Details</a>
                                    </div>
                                </div>
                            </div>
                        `;

                        container.innerHTML += cardHTML;
                    });
                })
                .catch(error => console.error("Error fetching data:", error));
        });