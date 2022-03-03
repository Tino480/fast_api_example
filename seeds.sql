-- subdireccion
insert into roles(id, name)
values (1, 'superadmin'), (2, 'director'), (3, 'admin'), (4, 'coordinator'), (5, 'superintendent'), (6, 'specialist');

-- users
insert into users(id, email, username, role_id, password)
values (1, 'tino@gmail.com', 'tino', 1, '$2b$12$HjnPg0YVmZkEwOovEpEYj.QrO1RyDnoFTV/PrqbfvClKOEQMRo7Tu');
