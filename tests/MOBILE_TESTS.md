Mobile testing checklist for the QR Attendance app

Purpose: manual test plan to validate responsive behavior and mobile slide-out menu.

Pages to test:
- /index.html
- /accountcreate.html
- /admin.html (login as admin@teacher/system123)
- /teacher.html (after teacher login)
- /student.html (after student login)

Test cases:
1. Global header and create button
   - Narrow viewport (<=480px): hamburger should be visible, create button scaled down, header fonts reduced.
   - Tap hamburger: side menu should slide in and an overlay should appear. Tapping overlay closes menu.
   - Rotate to landscape: menu closes automatically if viewport >1024px.

2. Login form (index.html)
   - At 375x812 (iPhone): inputs should span near full width, submit button full width, spacing maintained.
   - Ensure user_type toggles still work and submission posts to /api/login.

3. Account creation (/accountcreate.html)
   - Form inputs should be full width on small screens, labels readable, submit button full width.
   - Check that generated QR remains accessible after signup (signup flow uses query param signup=success).

4. Admin panel (/admin.html)
   - At small width, side-navbar hidden by default; hamburger toggles it. Content area uses full width.
   - Create Teacher form: inputs and button scaled, headings reduced.
   - Dashboard table: rows readable; padding reduced; horizontal scrolling avoided.

5. Teacher panel (/teacher.html)
   - QR scanner area scales to screen width; #qr-reader padding reduced on small screens.
   - Side menu toggles via hamburger; overlay blocks content when open.

6. Student panel (/student.html)
   - QR image scales to fit container; download button remains visible and tappable.
   - Status badge legible; attendance list entries readable and don't overlap.

Notes for testers:
- Use Chrome/Edge DevTools device toolbar or a physical device to validate touch interactions.
- If the side-navbar does not appear, ensure JavaScript is loaded (check console) and that the `.side-navbar` and `.hamburger` elements exist in the page.
- Report layout regressions: include screenshot, viewport size, and browser.

If you'd like, I can automate some of these smoke checks using Playwright or Puppeteer next. Request that and I'll scaffold tests.
