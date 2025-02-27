import React from 'react';

const Shipping = () => {
    return (
        <div>
            <h1>Shipping Information</h1>
            <form>
                <div>
                    <label htmlFor="name">Name:</label>
                    <input type="text" id="name" name="name" required />
                </div>
                <div>
                    <label htmlFor="address">Address:</label>
                    <input type="text" id="address" name="address" required />
                </div>
                <div>
                    <label htmlFor="city">City:</label>
                    <input type="text" id="city" name="city" required />
                </div>
                <div>
                    <label htmlFor="postalCode">Postal Code:</label>
                    <input type="text" id="postalCode" name="postalCode" required />
                </div>
                <div>
                    <label htmlFor="country">Country:</label>
                    <input type="text" id="country" name="country" required />
                </div>
                <button type="submit">Submit</button>
            </form>
        </div>
    );
};

export default Shipping;