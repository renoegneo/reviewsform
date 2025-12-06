/**
 * Конфигурация API
 * 
 * Для локальной разработки: http://127.0.0.1:8000
 * Для продакшена: просто замени на URL твоего хостинга
 */

const API_URL = 'https://reviewsform-production.up.railway.app/';

// Эндпоинты API
const API_ENDPOINTS = {
    reviews: `${API_URL}/reviews/`,
    stats: `${API_URL}/reviews/stats`,
};