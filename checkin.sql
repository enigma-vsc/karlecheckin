CREATE TABLE public.users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'customer' CHECK (role IN ('admin', 'customer'))
);


CREATE TABLE public.rooms (
    id SERIAL PRIMARY KEY,
    type VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    description TEXT,
    features TEXT, -- Optional comma-separated string for features
    availability BOOLEAN DEFAULT TRUE
);


CREATE TABLE public.bookings (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    room_id INT NOT NULL,
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    status VARCHAR(50) DEFAULT 'Confirmed' CHECK (status IN ('Confirmed', 'Cancelled')),

    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT fk_room FOREIGN KEY (room_id) REFERENCES rooms (id) ON DELETE CASCADE,
    CONSTRAINT unique_booking UNIQUE (room_id, check_in, check_out)
);




-- SET search_path = public, "$user", public; 
-- SELECT r.*
-- FROM rooms r
-- WHERE NOT EXISTS (
--     SELECT 1
--     FROM bookings b
--     WHERE b.room_id = r.id
--       AND b.check_in < '2024-12-10'
--       AND b.check_out >= '2024-12-08'
-- );