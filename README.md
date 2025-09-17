# KoLLaM – AI-Powered Kolam Design & Social Sharing Platform

KoLLaM is a full-stack project that combines traditional Indian kolam art with modern AI, computer vision, and social networking.
Users can:

- Generate unique kolam designs with mathematical based generation principles.

- Evaluate their own kolams using AI classification trained on real kolam principles.

- Share designs in a social media–style feed, with posts, images, and community interaction.

## Features

### Kolam Generator (FastAPI + Python)

- Procedurally generates kolam patterns using mathematical rules.

- Renders designs into images (PNG).

- API endpoint to fetch generated designs dynamically.

### Kolam Classifier

- Evaluates whether a user’s kolam follows traditional kolam principles based AI model.

- Built with ML/DL models trained on curated datasets.

### Social Media Platform (Next.js + Express + MongoDB)

- Users can post kolam designs, add descriptions, and attach images.

- Feed displays posts with author, timestamp, and design image.

- Community-driven sharing and showcasing.

## Tech Stack

### Frontend

- Next.js 15

- Apollo Client

- Tailwind CSS

### Backend

- Express.js

- MongoDB

- Mongoose

### AI & Kolam Generator

- FastAPI

- Python 3.10+

- matplotlib, numpy for rendering patterns

### Deployment

- AWS / Docker

- Load Balancer in front of Auth Service and API Service

- Optional GPU backend for ML models

## Inspiration

Kolam art is a centuries-old Indian tradition where women draw geometric patterns daily at their doorstep. KoLLaM reimagines this practice with AI creativity, community sharing, and modern digital expression.
