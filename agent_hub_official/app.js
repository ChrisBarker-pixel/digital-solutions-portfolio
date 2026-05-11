async function loadSaaSRoom() {
    // We only pull from a specific 'public_agents' collection in Firebase
    const snapshot = await firebase.database().ref('market_nodes').once('value');
    const agents = snapshot.val();

    const roomContainer = document.getElementById('node-room');

    // Manifest only the agents intended for the world to see
    Object.keys(agents).forEach(key => {
        const agent = agents[key];
        const node = document.createElement('div');
        node.className = 'saas-node-vessel';
        node.innerHTML = `<h3>${agent.name}</h3><p>${agent.utility}</p>`;
        roomContainer.appendChild(node);
    });
}.