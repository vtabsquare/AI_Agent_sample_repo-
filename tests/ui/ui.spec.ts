import { test, expect } from '@playwright/test';

test('server is running', async ({ page }) => {
  // Use the BASE_URL environment variable provided by releaseops_ci.py
  const baseURL = process.env.BASE_URL || 'http://localhost:8080';
  const response = await page.goto(baseURL);
  
  // Just check that it returns a 200-level status code (server is up)
  expect(response?.ok()).toBeTruthy();
});
