/**
 * Логика Dashboard (главной страницы)
 */

let ratingsChart = null;

// Маппинг для красивых названий категорий
const categoryLabels = {
    vehicle: 'Vehicle',
    driver: 'Driver',
    guide: 'Guide',
    accommodation: 'Accommodation',
    meals: 'Meals',
    overall: 'Overall'
};

// Маппинг оценок на звёзды
const ratingStars = {
    1: '★☆☆☆',
    2: '★★☆☆',
    3: '★★★☆',
    4: '★★★★'
};

/**
 * Загружает и отображает статистику
 */
async function loadStats() {
    try {
        const stats = await getStats();
        
        // Отображаем карточки со средними оценками
        displayStatsCards(stats);
        
        // Рисуем график
        displayChart(stats);
        
    } catch (error) {
        document.getElementById('statsGrid').innerHTML = 
            '<p class="error">Failed to load statistics</p>';
    }
}

/**
 * Отображает карточки со статистикой
 */
function displayStatsCards(stats) {
    const statsGrid = document.getElementById('statsGrid');
    
    const categories = ['vehicle', 'driver', 'guide', 'accommodation', 'meals', 'overall'];
    
    const cardsHTML = categories.map(category => {
        const value = stats.averages[category] || 0;
        const label = categoryLabels[category];
        
        return `
            <div class="stat-card">
                <span class="stat-value">${value.toFixed(1)}</span>
                <span class="stat-label">${label}</span>
            </div>
        `;
    }).join('');
    
    // Добавляем карточку с общим количеством
    const totalCard = `
        <div class="stat-card">
            <span class="stat-value">${stats.total}</span>
            <span class="stat-label">Total Reviews</span>
        </div>
    `;
    
    statsGrid.innerHTML = cardsHTML + totalCard;
}

/**
 * Отображает график распределения оценок
 */
function displayChart(stats) {
    const ctx = document.getElementById('ratingsChart').getContext('2d');
    
    // Уничтожаем старый график если есть
    if (ratingsChart) {
        ratingsChart.destroy();
    }
    
    // Подготавливаем данные для графика
    const categories = ['vehicle', 'driver', 'guide', 'accommodation', 'meals'];
    const datasets = [];
    
    // Создаём dataset для каждой оценки (1-4)
    const ratingColors = {
        1: '#e74c3c',  // красный
        2: '#f39c12',  // оранжевый
        3: '#3498db',  // синий
        4: '#2ecc71'   // зелёный
    };
    
    for (let rating = 1; rating <= 4; rating++) {
        const data = categories.map(category => {
            return stats.distribution[category][rating] || 0;
        });
        
        datasets.push({
            label: `${rating} ${rating === 4 ? 'High' : rating === 3 ? 'Good' : rating === 2 ? 'Average' : 'Low'}`,
            data: data,
            backgroundColor: ratingColors[rating]
        });
    }
    
    ratingsChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: categories.map(c => categoryLabels[c]),
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                x: {
                    stacked: true,
                },
                y: {
                    stacked: true,
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom'
                },
                title: {
                    display: false
                }
            }
        }
    });
}

/**
 * Загружает и отображает отзывы
 */
async function loadReviews() {
    try {
        const reviews = await getReviews({ limit: 50 });
        displayReviews(reviews);
    } catch (error) {
        document.getElementById('reviewsList').innerHTML = 
            '<p class="error">Failed to load reviews</p>';
    }
}

/**
 * Отображает список отзывов
 */
function displayReviews(reviews) {
    const reviewsList = document.getElementById('reviewsList');
    
    if (reviews.length === 0) {
        reviewsList.innerHTML = '<p>No reviews yet. Be the first to leave one!</p>';
        return;
    }
    
    const reviewsHTML = reviews.map(review => {
        const date = new Date(review.created_at).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
        
        return `
            <div class="review-card">
                <div class="review-header">
                    <div class="review-meta">
                        <div class="review-name">${review.name || 'Anonymous'}</div>
                        <div class="review-date">${date}</div>
                    </div>
                    <div class="review-overall">${review.overall_score?.toFixed(1) || 'N/A'}</div>
                </div>
                
                <div class="review-ratings">
                    <div class="rating-item">
                        <span class="rating-label">Vehicle</span>
                        <span class="rating-stars">${ratingStars[review.vehicle]}</span>
                    </div>
                    <div class="rating-item">
                        <span class="rating-label">Driver</span>
                        <span class="rating-stars">${ratingStars[review.driver]}</span>
                    </div>
                    <div class="rating-item">
                        <span class="rating-label">Guide</span>
                        <span class="rating-stars">${ratingStars[review.guide]}</span>
                    </div>
                    <div class="rating-item">
                        <span class="rating-label">Accommodation</span>
                        <span class="rating-stars">${ratingStars[review.accommodation]}</span>
                    </div>
                    <div class="rating-item">
                        <span class="rating-label">Meals</span>
                        <span class="rating-stars">${ratingStars[review.meals]}</span>
                    </div>
                </div>
                
                ${review.comment ? `
                    <div class="review-comment">
                        "${review.comment}"
                    </div>
                ` : ''}
            </div>
        `;
    }).join('');
    
    reviewsList.innerHTML = reviewsHTML;
}

/**
 * Инициализация при загрузке страницы
 */
document.addEventListener('DOMContentLoaded', () => {
    loadStats();
    loadReviews();
});