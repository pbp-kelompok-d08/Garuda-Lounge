function showToast(title, message, type = 'normal', duration = 3000) {
    const toastComponent = document.getElementById('toast-component');
    const toastTitle = document.getElementById('toast-title');
    const toastMessage = document.getElementById('toast-message');
    const toastIcon = document.getElementById('toast-icon');

    if (!toastComponent) return;

    // Hapus semua style class lama
    toastComponent.classList.remove(
        'bg-[#E7E3DD]', 'border-[#AA1515]', 'text-[#111111]',
        'bg-[#FFFFFF]', 'border-[#AA1515]', 'text-[#AA1515]',
        'bg-[#FFFFFF]', 'border-[#111111]', 'text-[#111111]'
    );

    // Reset inline style & icon
    toastComponent.style.border = '';
    toastIcon.textContent = '';

    // Warna & ikon sesuai tipe
    if (type === 'success') {
        toastComponent.style.backgroundColor = '#E7E3DD';   // Cream lembut
        toastComponent.style.border = '2px solid #AA1515';  // Merah khas
        toastComponent.style.color = '#111111';
        toastIcon.textContent = '✅';
    } 
    else if (type === 'error') {
        toastComponent.style.backgroundColor = '#FFFFFF';
        toastComponent.style.border = '2px solid #AA1515';
        toastComponent.style.color = '#AA1515';
        toastIcon.textContent = '❌';
    } 
    else {
        toastComponent.style.backgroundColor = '#FFFFFF';
        toastComponent.style.border = '2px solid #111111';
        toastComponent.style.color = '#111111';
        toastIcon.textContent = 'ℹ️';
    }

    // Isi teks
    toastTitle.textContent = title;
    toastMessage.textContent = message;

    // Animasi muncul (pakai class Tailwind)
    toastComponent.classList.remove('opacity-0', 'translate-y-64');
    toastComponent.classList.add('opacity-100', 'translate-y-0');

    // Hilang otomatis
    setTimeout(() => {
        toastComponent.classList.remove('opacity-100', 'translate-y-0');
        toastComponent.classList.add('opacity-0', 'translate-y-64');
    }, duration);
}