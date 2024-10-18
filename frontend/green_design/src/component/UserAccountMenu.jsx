import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Dropdown } from 'react-bootstrap';
import { getAuth, signOut } from "firebase/auth";

const UserAccountMenu = () => {
    const [user, setUser] = useState(null);
    const navigate = useNavigate();
    const auth = getAuth();

    useEffect(() => {
        const unsubscribe = auth.onAuthStateChanged((user) => {
            if (user) {
                setUser(user);
            } else {
                setUser(null);
            }
        });

        return () => unsubscribe();
    }, [auth]);

    const handleLogout = async () => {
        try {
            await signOut(auth);
            navigate('/login');
        } catch (error) {
            console.error("Error signing out: ", error);
        }
    };

    if (!user) return null;

    return (
        <Dropdown>
            <Dropdown.Toggle variant="link" id="dropdown-basic" className="p-0">
                <img 
                    src={user.photoURL} 
                    alt="User" 
                    style={{ width: '32px', height: '32px', borderRadius: '50%' }} 
                />
            </Dropdown.Toggle>

            <Dropdown.Menu>
                <Dropdown.ItemText>{user.displayName}</Dropdown.ItemText>
                <Dropdown.Divider />
                <Dropdown.Item onClick={handleLogout}>Logout</Dropdown.Item>
            </Dropdown.Menu>
        </Dropdown>
    );
};

export default UserAccountMenu;