(() => {
    const shell = document.querySelector('.chat-shell');
    if (!shell) {
        return;
    }

    const roomId = shell.dataset.roomId;
    const userId = shell.dataset.userId;

    if (!userId) {
        return;
    }

    const chatMessages = document.getElementById('chatMessages');
    const chatForm = document.getElementById('chatForm');
    const chatText = document.getElementById('chatText');
    const chatImage = document.getElementById('chatImage');
    const chatAudio = document.getElementById('chatAudio');

    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const socket = new WebSocket(`${protocol}://${window.location.host}/ws/chat/${roomId}/`);

    const scrollToBottom = () => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    const createMessageElement = (data) => {
        const wrapper = document.createElement('article');
        wrapper.className = 'chat-message';
        if (String(data.sender_id) === String(userId)) {
            wrapper.classList.add('self');
        }

        const meta = document.createElement('div');
        meta.className = 'meta';

        const sender = document.createElement('strong');
        sender.textContent = data.sender;

        const time = document.createElement('span');
        const date = new Date(data.created_at);
        time.textContent = date.toLocaleTimeString('pt-BR', {
            hour: '2-digit',
            minute: '2-digit',
        });

        meta.appendChild(sender);
        meta.appendChild(time);
        wrapper.appendChild(meta);

        if (data.message_type === 'text') {
            const text = document.createElement('p');
            text.textContent = data.text;
            wrapper.appendChild(text);
        }

        if (data.message_type === 'image' && data.file_url) {
            const img = document.createElement('img');
            img.src = data.file_url;
            img.alt = 'Imagem enviada';
            wrapper.appendChild(img);
        }

        if (data.message_type === 'audio' && data.file_url) {
            const audio = document.createElement('audio');
            audio.controls = true;
            audio.src = data.file_url;
            wrapper.appendChild(audio);
        }

        return wrapper;
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        const messageEl = createMessageElement(data);
        chatMessages.appendChild(messageEl);
        scrollToBottom();
    };

    socket.onopen = () => {
        scrollToBottom();
    };

    chatForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const text = chatText.value.trim();
        if (!text) {
            return;
        }
        socket.send(JSON.stringify({
            message_type: 'text',
            text,
        }));
        chatText.value = '';
    });

    const sendFileMessage = (file, messageType) => {
        const reader = new FileReader();
        reader.onload = () => {
            socket.send(JSON.stringify({
                message_type: messageType,
                file_name: file.name,
                file_data: reader.result,
            }));
        };
        reader.readAsDataURL(file);
    };

    chatImage.addEventListener('change', () => {
        const file = chatImage.files[0];
        if (!file) {
            return;
        }
        sendFileMessage(file, 'image');
        chatImage.value = '';
    });

    chatAudio.addEventListener('change', () => {
        const file = chatAudio.files[0];
        if (!file) {
            return;
        }
        sendFileMessage(file, 'audio');
        chatAudio.value = '';
    });
})();
