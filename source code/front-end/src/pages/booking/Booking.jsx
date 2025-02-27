import React, { useState } from 'react';

const Booking = () => {
    const [name, setName] = useState('');
    const [date, setDate] = useState('');
    const [time, setTime] = useState('');
    const [guests, setGuests] = useState(1);

    const handleSubmit = (e) => {
        e.preventDefault();
        alert(`Booking confirmed for ${name} on ${date} at ${time} for ${guests} guests.`);
    };

    return (
        <div>
            <h1>Restaurant Booking</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Name:</label>
                    <input 
                        type="text" 
                        value={name} 
                        onChange={(e) => setName(e.target.value)} 
                        required 
                    />
                </div>
                <div>
                    <label>Date:</label>
                    <input 
                        type="date" 
                        value={date} 
                        onChange={(e) => setDate(e.target.value)} 
                        required 
                    />
                </div>
                <div>
                    <label>Time:</label>
                    <input 
                        type="time" 
                        value={time} 
                        onChange={(e) => setTime(e.target.value)} 
                        required 
                    />
                </div>
                <div>
                    <label>Number of Guests:</label>
                    <input 
                        type="number" 
                        value={guests} 
                        onChange={(e) => setGuests(e.target.value)} 
                        min="1" 
                        required 
                    />
                </div>
                <button type="submit">Book Now</button>
            </form>
        </div>
    );
};

export default Booking;