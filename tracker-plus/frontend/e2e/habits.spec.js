import { test, expect } from '@playwright/test'

const backendBase = 'http://localhost:5000'

test.beforeEach(async ({ request }) => {
  await request.delete(`${backendBase}/test/reset`)
})

test('E-01: criar hábito aparece na lista', async ({ page }) => {
  await page.goto('/')
  await page.getByTestId('habit-name-input').fill('Meditar')
  await page.getByTestId('add-habit-btn').click()
  await expect(page.locator('[data-testid^="habit-card-"]')).toBeVisible()
  await expect(page.getByText('Meditar')).toBeVisible()
})

test('E-02: formulário bloqueia nome vazio', async ({ page }) => {
  await page.goto('/')
  await page.getByTestId('add-habit-btn').click()
  await expect(page.getByTestId('form-error')).toBeVisible()
  await expect(page.locator('[data-testid^="habit-card-"]')).toHaveCount(0)
})

test('E-03: marcar concluído desabilita o botão', async ({ page }) => {
  await page.goto('/')
  await page.getByTestId('habit-name-input').fill('Exercício')
  await page.getByTestId('add-habit-btn').click()
  const completeBtn = page.locator('[data-testid^="complete-btn-"]').first()
  await completeBtn.waitFor({ state: 'visible' })
  await completeBtn.click()
  await expect(completeBtn).toBeDisabled()
})

test('E-04: não permite concluir duas vezes no mesmo dia', async ({ page }) => {
  await page.goto('/')
  await page.getByTestId('habit-name-input').fill('Yoga')
  await page.getByTestId('add-habit-btn').click()
  const completeBtn = page.locator('[data-testid^="complete-btn-"]').first()
  await completeBtn.waitFor({ state: 'visible' })
  await completeBtn.click()

  await expect(page.getByTestId('already-completed-msg')).toBeVisible()
  await expect(completeBtn).toBeDisabled()
})

test('E-05: hábito concluído aparece no leaderboard', async ({ page }) => {
  await page.goto('/')
  await page.getByTestId('habit-name-input').fill('Ler')
  await page.getByTestId('add-habit-btn').click()
  const completeBtn = page.locator('[data-testid^="complete-btn-"]').first()
  await completeBtn.waitFor({ state: 'visible' })
  await completeBtn.click()

  await page.goto('/stats')
  await expect(page.getByTestId('leaderboard')).toBeVisible()
  await expect(page.getByText('Ler')).toBeVisible()
})
