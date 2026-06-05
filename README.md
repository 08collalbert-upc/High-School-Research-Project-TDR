# Virtual Assistant for Individuals with Autism Spectrum Disorder (ASD)

## Project Overview
This repository contains the full functional implementation and front-end architecture of **TDR_1**, an AI-powered voice and text assistant tailored specifically for individuals with Autism Spectrum Disorder (ASD). This software serves as the practical component of my High School Research Project (**Treball de Recerca - TDR**) during the 2nd year of Bachillerato.

The main objective is to reduce cognitive overload and conversational ambiguity by applying custom prompt parameters, structured turn-by-turn interactions, and multi-modal integration (Text-to-Speech and Speech-to-Text).

## Technical Architecture & Flow
The application bridges a responsive web interface with advanced AI models through a local server:
1. **User Input:** Audio recording (via browser microphone) or direct text input.
2. **Speech-to-Text (STT):** Processed via OpenAI's **Whisper** API to convert voice inputs into accurate text.
3. **Core LLM & Prompt Engineering:** Handled by **GPT-4**, utilizing optimized system parameters (`temperature=0.2`, `top_p=0.5`) to enforce structured, literal, and step-by-step responses.
4. **Text-to-Speech (TTS):** Generated via **ElevenLabs Multilingual v2** for natural, stable, and low-latency audio output.
5. **Deployment:** Served locally utilizing a **Flask** backend framework in Python.

## Repository Structure
* `/backend` (or root script): 
  * Core application logic handling routing, endpoints (`/missatge`), and API orchestration.
* `/frontend`:
  * `index.html`: Core UI layout, structuring text areas, and embedding script logics for audio blob processing (base64 decoding).
  * `style.css`: UI/UX styling optimized for interface accessibility.
* `.env`: Environment configurations for credential management *(Note: Keep actual API keys hidden for security).*

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/](https://github.com/)[YOUR_USERNAME]/[REPOSITORY_NAME].git
