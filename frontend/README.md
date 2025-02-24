# FreshLens Frontend

## Table of Contents
- [Homepage](#page-1-homepage)
- [Real-Time View](#page-2-real-time-view)
- [Detailed Fridge View](#page-3-detailed-fridge-view)
- [Account & Settings](#page-4-account--settings)
- [Getting Started](#getting-started)
- [Contributing](#contributing)

---

## Page 1: Homepage

### Overview
- **Notifications:** Displays alerts for items about to expire, plus other important app notifications.
- **Storage Tips:** Provides general storage advice (e.g., from USDA) to help you keep food fresh longer.
- **Analytics:** Shows key metrics including:
  - **Fridge Freshness Score:** A percentage-based rating of overall freshness.
  - **Money Saved Per Week:** Helps you track savings and encourages cost-effective habits.
- **Shopping Cart Recommendations:** Uses AI to suggest items based on your previous shopping and throwaway habits.

### Key Components
1. **Notifications Banner:** Highlights items at risk of expiring and other critical updates.
2. **Storage Tip Card:** Displays best practices for storing items (e.g., proper container usage, recommended temperature).
3. **Analytics Widgets:**
   - **Fridge Freshness Gauge:** A circular progress bar showing the current freshness score.
   - **Money Saved Chart:** A bar chart tracking your weekly savings.
4. **Shopping Cart Button:** Redirects to your AI-driven shopping list with recommended items.

---

## Page 2: Real-Time View

Stay connected to your fridge from anywhere by viewing live camera feeds. Whether you’re at work or shopping for groceries, you can quickly check what items are inside without opening the fridge door.

### Key Features
- **Remote Monitoring:** View your fridge’s contents in near real-time from any location.
- **Item Detection Overlays:** Automatically highlight fruits, vegetables, and other items with bounding boxes for easy identification.
- **Timestamped Snapshots:** Each image displays the exact time it was captured.
- **Refetch Image Button:** Retrieve a fresh snapshot on demand. Otherwise, the images you see are the last frames captured from the motion-based video feed.


<img src="https://github.com/user-attachments/assets/d5e7b11b-de3e-4722-a89e-518d41b9386b" alt="App Screenshot" width="300" />

<img src="https://github.com/user-attachments/assets/75154230-3f2c-4fa9-a979-4aca626ba1c8" alt="App Screenshot" width="300" />

---

## Page 3: Detailed Fridge View

Dive deeper into the contents of your fridge by selecting specific categories, products, and individual items. This page provides comprehensive details and AI-powered recipe suggestions to help you make the most of your ingredients before they expire.

### Key Features
1. **Fridge Selection:** Pick which fridge you want to inspect (e.g., Home or Office).
2. **Category Browsing:** Filter items by categories such as Dairy, Vegetables, Beverages, Meat, etc.
3. **Recipe Suggestions:** Ask AI for recipe ideas that incorporate items nearing expiration.
4. **Product Listings:** View available products in each category.
5. **Item Details:**
   - **Expiration Tracking:** See when each item was entered and when it will expire (with alerts if it's already expired).
   - **Nutritional Facts:** Get essential nutrition data (e.g., calories, protein, fat).
   - **Storage Tips:** Learn best practices for storing each product.
   - **Average Price:** Check the typical cost of the product. *(Future plans include integration with your supermarket or manual price entry.)*
<img src="https://github.com/user-attachments/assets/0bdd614d-49f4-425c-831f-9051ab8a72ba" alt="App Screenshot" width="300" />
<img src="https://github.com/user-attachments/assets/7463dbda-96fe-42ba-8498-5578081a027b" alt="App Screenshot" width="300" />
<img src="https://github.com/user-attachments/assets/23f84316-cff1-4e63-aaec-714072b8b5c6" alt="App Screenshot" width="300" />
<img src="https://github.com/user-attachments/assets/4490030b-125f-40a8-9d70-61b5aa2e44e2" alt="App Screenshot" width="300" />
<img src="https://github.com/user-attachments/assets/75845c2e-984a-4ba0-b0b0-a33ba7a39395" alt="App Screenshot" width="300" />
<img src="https://github.com/user-attachments/assets/b0d97cef-959d-4013-9002-5e33c00a83b0" alt="App Screenshot" width="300" />
<img src="https://github.com/user-attachments/assets/bd206e77-85ed-4c86-a6e3-d01d3a7ce4e3" alt="App Screenshot" width="300" />
<img src="https://github.com/user-attachments/assets/de415ccc-6a71-4f22-83c6-c95c0790eec5" alt="App Screenshot" width="300" />

---

## Page 4: Account & Settings

Manage your personal information, subscription plan, and fridge configurations all in one place. This page also provides an option to log out, ensuring secure access to your account.

### Key Features
1. **Subscription Management:** View and update your plan (Free, Plus, or Premium).
2. **Add/Remove Fridges:** Easily create new fridge profiles or remove old ones.
3. **Future Customizations:**
   - **Groceries & Shopping Preferences:** Specify where you typically shop to tailor price and availability information.
   - **Notification Frequency:** Choose how often you want to receive alerts about expiring items or other updates.
   - **Camera Configurations:** Customize camera settings, motion detection sensitivity, and more.
4. **Logout:** Securely end your session when you’re done.

This page will continue to evolve with more advanced personalization and user preferences. 

<img src="https://github.com/user-attachments/assets/a37edf5c-0154-455f-afbf-ea5ba73e3eb5" alt="App Screenshot" width="300" />

---

## Getting Started

Follow the steps below to set up and run the FreshLens frontend locally.

### Prerequisites
- [Node.js](https://nodejs.org/) (v14 or higher recommended)
- [npm](https://www.npmjs.com/) or [Yarn](https://yarnpkg.com/) (your choice of package manager)

### 1. Clone the Repository
```bash
git clone https://github.com/tomerud/Freshlens.git
cd frontend
```
### 2. run the frontend server
```bash
npm run dev
```
