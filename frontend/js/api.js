/**
 * API клиент для работы с бэкендом
 * Все функции асинхронные (async/await)
 */

/**
 * Создать новый отзыв
 * @param {Object} reviewData - данные отзыва
 * @returns {Promise<Object>} созданный отзыв
 */
async function createReview(reviewData) {
    try {
        const response = await fetch(API_ENDPOINTS.reviews, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(reviewData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to create review');
        }

        return await response.json();
    } catch (error) {
        console.error('Error creating review:', error);
        throw error;
    }
}

/**
 * Получить список отзывов
 * @param {Object} params - параметры фильтрации
 * @returns {Promise<Array>} список отзывов
 */
async function getReviews(params = {}) {
    try {
        // Формируем query string (например: ?skip=0&limit=100&tour_id=tour123)
        const queryParams = new URLSearchParams(params);
        const url = `${API_ENDPOINTS.reviews}?${queryParams}`;

        const response = await fetch(url);

        if (!response.ok) {
            throw new Error('Failed to fetch reviews');
        }

        return await response.json();
    } catch (error) {
        console.error('Error fetching reviews:', error);
        throw error;
    }
}

/**
 * Получить статистику
 * @returns {Promise<Object>} объект со статистикой
 */
async function getStats() {
    try {
        const response = await fetch(API_ENDPOINTS.stats);

        if (!response.ok) {
            throw new Error('Failed to fetch stats');
        }

        return await response.json();
    } catch (error) {
        console.error('Error fetching stats:', error);
        throw error;
    }
}