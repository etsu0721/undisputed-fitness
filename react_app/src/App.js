import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  // Get exercise data from backend
  const rootElement = document.getElementById("root");
  const exercisesJSON = rootElement.getAttribute("data-exercises");
  const [deck, setDeck] = useState(generateDeck(JSON.parse(exercisesJSON)));
  const [shown, setShown] = useState([]);

  function generateDeck(exercises) {
    const suits = ['♠', '♣', '♦', '♥'];
    let pairings = [];
    for (let i = 0; i < 4; i++) {
      pairings.push({value: suits[i] + exercises[i]["name"], zIndex: 0});
    }
    let deck = Array(13).fill(pairings).flat();
    return shuffle(deck);
  }

  function shuffle(array) {
    let currentIndex = array.length, randomIndex;

    while (currentIndex !== 0) {
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex--;

      [array[currentIndex], array[randomIndex]] = [array[randomIndex], array[currentIndex]];
    }

    return array;
  }

  const handleCardClick = () => {
    if (deck.length === 0) return;

    let currentDeck = [...deck];
    let card = currentDeck.pop();

    card.zIndex = new Date().getTime();

    setShown([...shown, card]);
    setDeck(currentDeck);
  };

  return (
    <div className="container">
      <div className="deck-area" onClick={handleCardClick}>
        {deck.map(card => (
          <div key={card.value} className="remaining-card">
            <div className="card-back"></div>
            <div className="card-front">
              {card.value}
            </div>
          </div>
        ))}
      </div>

      <div className="discard-pile">
        {shown.map(card => (
          <div key={card.value} className="shown-card" style={{ zIndex: card.zIndex }}>
            <div className="card-back"></div>
            <div className="card-front">
              {card.value}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;