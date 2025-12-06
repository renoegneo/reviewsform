/**
 * Логика формы создания отзыва
 */

/**
 * Показывает уведомление
 */
function showNotification(message, type = 'success') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification ${type} show`;
    
    // Скрываем через 5 секунд
    setTimeout(() => {
        notification.classList.remove('show');
    }, 5000);
}

/**
 * Собирает данные формы
 */
function getFormData() {
    const form = document.getElementById('reviewForm');
    const formData = new FormData(form);
    
    // Преобразуем в объект
    const data = {
        vehicle: parseInt(formData.get('vehicle')),
        driver: parseInt(formData.get('driver')),
        guide: parseInt(formData.get('guide')),
        accommodation: parseInt(formData.get('accommodation')),
        meals: parseInt(formData.get('meals')),
        comment: document.getElementById('comment').value.trim() || null,
        name: document.getElementById('name').value.trim() || null,
        email: document.getElementById('email').value.trim() || null,
        tour_id: document.getElementById('tour_id').value.trim() || null,
    };
    
    return data;
}

/**
 * Валидация формы
 */
function validateForm(data) {
    // Проверяем что все оценки выставлены (1-4)
    const ratings = ['vehicle', 'driver', 'guide', 'accommodation', 'meals'];
    
    for (const rating of ratings) {
        if (!data[rating] || data[rating] < 1 || data[rating] > 4) {
            return {
                valid: false,
                message: `Please select a rating for ${rating}`
            };
        }
    }
    
    // Проверяем email если указан
    if (data.email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(data.email)) {
            return {
                valid: false,
                message: 'Please enter a valid email address'
            };
        }
    }
    
    return { valid: true };
}

/**
 * Сброс формы
 */
function resetForm() {
    document.getElementById('reviewForm').reset();
}

/**
 * Обработчик отправки формы
 */
async function handleSubmit(e) {
    e.preventDefault();
    
    // Собираем данные
    const data = getFormData();
    
    // Валидация
    const validation = validateForm(data);
    if (!validation.valid) {
        showNotification(validation.message, 'error');
        return;
    }
    
    // Отключаем кнопку отправки (чтобы не отправляли дважды)
    const submitBtn = e.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.textContent = 'Submitting...';
    
    try {
        // Отправляем на сервер
        await createReview(data);
        
        // Показываем успех
        showNotification('Thank you! Your review has been submitted successfully.', 'success');
        
        // Сбрасываем форму
        resetForm();
        
        // Через 2 секунды редиректим на главную
        setTimeout(() => {
            window.location.href = 'index.html';
        }, 2000);
        
    } catch (error) {
        // Показываем ошибку
        showNotification(
            `Failed to submit review: ${error.message}. Please try again.`,
            'error'
        );
        
        // Включаем кнопку обратно
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
    }
}

/**
 * Инициализация при загрузке страницы
 */
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('reviewForm');
    form.addEventListener('submit', handleSubmit);
});