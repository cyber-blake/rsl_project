      // Обработка формы комментариев
      document
        .getElementById("commentForm")
        .addEventListener("submit", function (e) {
          e.preventDefault();

          // Получаем данные из формы
          const name = document.getElementById("name").value;
          const commentText = document.getElementById("comment").value;

          // Создаем новый элемент комментария
          const commentList = document.querySelector(".comments-list");
          const newComment = document.createElement("div");
          newComment.className = "comment";

          // Генерируем дату
          const now = new Date();
          const dateString =
            now.toLocaleDateString("ru-RU") +
            ", " +
            now.toLocaleTimeString("ru-RU", {
              hour: "2-digit",
              minute: "2-digit",
            });

          // Получаем инициалы для аватара
          const initials = name
            .split(" ")
            .map((n) => n[0])
            .join("")
            .toUpperCase();

          // Заполняем новый комментарий
          newComment.innerHTML = `
                <div class="comment-header">
                    <div class="comment-author">
                        <div class="author-avatar">${initials}</div>
                        <div class="author-info">
                            <h4>${name}</h4>
                            <div class="comment-date">${dateString}</div>
                        </div>
                    </div>
                </div>
                <div class="comment-text">
                    ${commentText}
                </div>
                <div class="comment-reply">
                    <button class="reply-btn">Ответить</button>
                </div>
            `;

          // Добавляем новый комментарий в начало списка
          commentList.prepend(newComment);

          // Обновляем заголовок с количеством комментариев
          const commentsTitle = document.querySelector(".comments-title");
          const currentCount = parseInt(
            commentsTitle.textContent.match(/\d+/)[0]
          );
          commentsTitle.textContent = `Комментарии (${currentCount + 1})`;

          // Сбрасываем форму
          this.reset();

          // Показываем сообщение об успехе
          alert("Ваш комментарий успешно добавлен!");
        });

      // Обработка кнопок "Ответить"
      document.addEventListener("click", function (e) {
        if (e.target && e.target.classList.contains("reply-btn")) {
          const comment = e.target.closest(".comment");
          const authorName = comment.querySelector("h4").textContent;

          // Создаем текстовое поле для ответа
          const replyForm = document.createElement("div");
          replyForm.className = "comment-reply-form";
          replyForm.innerHTML = `
                    <div class="form-group">
                        <textarea placeholder="Ответить ${authorName}..." rows="3" class="reply-textarea"></textarea>
                    </div>
                    <button class="submit-btn reply-submit">Отправить ответ</button>
                    <button class="reply-cancel" style="margin-left: 10px; background: #6c757d; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">Отмена</button>
                `;

          // Вставляем форму после кнопки "Ответить"
          const replySection = comment.querySelector(".comment-reply");
          replySection.appendChild(replyForm);

          // Скрываем кнопку "Ответить"
          e.target.style.display = "none";

          // Обработка отправки ответа
          const submitBtn = replyForm.querySelector(".reply-submit");
          const cancelBtn = replyForm.querySelector(".reply-cancel");

          submitBtn.addEventListener("click", function () {
            const replyText = replyForm.querySelector(".reply-textarea").value;
            if (replyText.trim()) {
              alert(
                `Ответ для ${authorName}: ${replyText}\n\nВ реальном приложении этот ответ будет сохранен в базе данных.`
              );
              replyForm.remove();
              e.target.style.display = "block";
            }
          });

          cancelBtn.addEventListener("click", function () {
            replyForm.remove();
            e.target.style.display = "block";
          });
        }
      })