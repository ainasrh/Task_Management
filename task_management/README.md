## Task Management API

### Authentication
- Uses JWT via `rest_framework_simplejwt`.
- Obtain tokens via `POST /login/`.
- Include Access token in Authorization header: `Authorization: Bearer <token>`.

### Public Endpoints
- POST `register/` – Register a new user
  - Body: { username, email, password, confirm_password }
  - 201 Created: user data
- POST `login/` – Obtain JWT tokens
  - Body: { username, password }
  - 200 OK: { message, user, refresh_token, access_token }

### User Profile (JWT required)
- GET `profile/` – Get current user profile
- PATCH `profile/` – Update current user fields
  - Body (partial): { username?, email? }

### Task APIs (JWT required)
- GET `list-task/` – List tasks assigned to the authenticated user
- PUT `update-task/<int:pk>/` – Update a task assigned to the user
  - Body (partial): { status?, worked_hours?, completion_report? }
  - Validation: If status == completed, both worked_hours and completion_report are required

### SuperAdmin Views (session auth via views; template pages)
- GET `user/<str:role>/` (name: `all-users`) – List users by role
- POST `create-user/` (name: `create-user`) – Create a user (form)
- POST `delete-user/<int:id>/` (name: `delete-user`) – Delete a user
- POST `assign-role/<int:user_id>/` (name: `assign-role`) – Change user role
- POST `assign-admin/<int:user_id>/` (name: `assign-admin`) – Assign an admin to a user
- GET `all-task/` (name: `all-task`) – List all tasks
- GET/POST `create-task/` (name: `create-task`) – Create a task (form)
- GET/POST `edit-task/<int:task_id>/` (name: `superadmin-edit-task`) – Edit task (form)
- GET `completed-tasks/` (name: `completed-tasks`) – List completed tasks
- GET `superadmin-dashboard/` (name: `superadmin_dashboard`) – Superadmin dashboard
- GET `no-access/` (name: `no_access`) – No access page


