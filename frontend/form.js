document.getElementById('lead-form')
  .addEventListener('submit', async (e) => {
    e.preventDefault();

    const btn = document.getElementById('submit-btn');
    const msg = document.getElementById('msg');

    // Désactiver le bouton pendant l'envoi
    btn.disabled = true;
    btn.textContent = 'Envoi en cours...';
    msg.className = 'msg hidden';

    // Construire l'objet de données
    const data = {
        name:    e.target.name.value.trim(),
        email:   e.target.email.value.trim(),
        phone:   e.target.phone.value.trim() || null,
        message: e.target.message.value.trim()
    };

    try {
        const res = await fetch('/api/leads', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const json = await res.json();

        if (res.ok) {
            // Succès ou doublon — même message pour le lead
            msg.textContent =
                'Merci ! Notre équipe vous contacte sous 24h.';
            msg.className = 'msg success';
            e.target.reset();
        } else {
            msg.textContent =
                'Une erreur est survenue. Veuillez réessayer.';
            msg.className = 'msg error';
        }

    } catch (err) {
        // Erreur réseau
        msg.textContent =
            'Problème de connexion. Veuillez réessayer.';
        msg.className = 'msg error';

    } finally {
        btn.disabled = false;
        btn.textContent = 'Envoyer ma demande';
    }
});