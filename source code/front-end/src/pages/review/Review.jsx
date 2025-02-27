import React, { useState } from 'react';

const Review = () => {
    const [reviews, setReviews] = useState([]);
    const [newReview, setNewReview] = useState('');

    const handleInputChange = (e) => {
        setNewReview(e.target.value);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (newReview.trim()) {
            setReviews([...reviews, newReview]);
            setNewReview('');
        }
    };

    return (
        <div>
            <h1>Customer Reviews</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={newReview}
                    onChange={handleInputChange}
                    placeholder="Write a review"
                />
                <button type="submit">Submit</button>
            </form>
            <ul>
                {reviews.map((review, index) => (
                    <li key={index}>{review}</li>
                ))}
            </ul>
        </div>
    );
};

export default Review;