
import { initializeApp } from
  "https://www.gstatic.com/firebasejs/13.3.0/firebase-app.js";

import {
  getAI,
  getGenerativeModel,
  GoogleAIBackend
} from "https://www.gstatic.com/firebasejs/13.3.0/firebase-ai.js";

// Configuração do projeto Firebase
const firebaseConfig = {
  apiKey: "AIzaSyBmokUBfByALGwePY61auWKKivbfwvhrLk",
  authDomain: "paginaestudosia.firebaseapp.com",
  projectId: "paginaestudosia",
  storageBucket: "paginaestudosia.firebasestorage.app",
  messagingSenderId: "183138205235",
  appId: "1:183138205235:web:34753b2cd8435039022d46"
};

// Inicializa o Firebase
const firebaseApp = initializeApp(firebaseConfig);

// Inicializa o Firebase AI Logic
const ai = getAI(firebaseApp, {
  backend: new GoogleAIBackend()
});

// Cria o modelo Gemini
const model = getGenerativeModel(ai, {
  model: "gemini-3.8-flash"
});

// Função pública para conversar com o Gemini
export async function perguntarGemini(pergunta, contexto = "") {
  if (!pergunta || !pergunta.trim()) {
    throw new Error("Digite uma pergunta.");
  }

  const prompt = `
Você é um tutor acadêmico da Biblioteca de Estudos de Direito.

Sua função é ajudar o estudante a compreender os conteúdos
jurídicos com clareza, rigor conceitual e linguagem didática.

Use o contexto fornecido quando disponível.
Não invente referências legais ou doutrinárias.
Diferencie informações confirmadas de interpretações.

CONTEXTO DO ESTUDO:
${contexto}

PERGUNTA DO ESTUDANTE:
${pergunta}
`;

  const resultado = await model.generateContent(prompt);

  return resultado.response.text();
}
