import React from 'react';

const Menu = () => {
    const menuItems = [
        { name: 'Pizza', price: '$10' },
        { name: 'Burger', price: '$8' },
        { name: 'Pasta', price: '$12' },
        { name: 'Salad', price: '$7' },
    ];

    return (
        <div>
            <h1>Menu</h1>
            <ul>
                {menuItems.map((item, index) => (
                    <li key={index}>
                        {item.name} - {item.price}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Menu;