export default function renderMessage(text, messageTag='success') {
    const element = document.getElementById('messages')
    element.innerHTML = `
        <div class="alert alert-${messageTag}" role="alert">
            <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
            ${text}
        </div>
    `
}
