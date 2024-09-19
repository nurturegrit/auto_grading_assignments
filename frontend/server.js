/**const express = require('express');
const path = require('path');
const multer = require('multer');
const fs = require('fs');

const app = express();
const port = 4001;

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// Set storage engine for multer
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'uploads'); // Save files to 'uploads' folder
    },
    filename: function (req, file, cb) {
        // Use the original file name
        const originalName = file.originalname;
        cb(null, originalName);
    }
});

// Initialize multer with the defined storage
const upload = multer({ storage: storage });

// Ensure the 'uploads' folder exists (create it if it doesn't)
const uploadsDir = path.join(__dirname, 'uploads');
if (!fs.existsSync(uploadsDir)) {
    fs.mkdirSync(uploadsDir);
}

// Route to handle file uploads from upload.html
app.post('/upload_handler', upload.any(), (req, res) => {
    if (!req.files || req.files.length === 0) {
        return res.status(400).send('Please select a file');
    }
    console.log('Files uploaded:', req.files);
    res.send('Files uploaded successfully!');
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});**/

/*const express = require('express');
const path = require('path');
const multer = require('multer');
const fs = require('fs');

const app = express();
const port = 4013;

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// Set storage engine for multer
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'uploads'); // Save files to 'uploads' folder
    },
    filename: function (req, file, cb) {
        // Use the original file name
        const originalName = file.originalname;
        cb(null, originalName);
    }
});

// Initialize multer with the defined storage
const upload = multer({ storage: storage });

// Ensure the 'uploads' folder exists (create it if it doesn't)
const uploadsDir = path.join(__dirname, 'uploads');
if (!fs.existsSync(uploadsDir)) {
    fs.mkdirSync(uploadsDir);
}

// Route to handle file uploads from upload.html
app.post('/upload_handler', upload.any(), (req, res) => {
    // Check if files were uploaded
    if (!req.files || req.files.length === 0) {
        return res.status(400).send('Please select a file');
    }

    console.log('Files uploaded:', req.files);
    res.send('Files uploaded successfully!');
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
*/
const express = require('express');
const path = require('path');
const multer = require('multer');
const fs = require('fs');

const app = express();
const port = 4021;

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// Set storage engine for multer
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        // Ensure the user's folder exists
        const userFolder = path.join('uploads', req.body.userId || 'default');
        if (!fs.existsSync(userFolder)) {
            fs.mkdirSync(userFolder, { recursive: true });
        }
        cb(null, userFolder); // Save files to the user's folder
    },
    filename: function (req, file, cb) {
        // Use the original file name
        const originalName = file.originalname;
        cb(null, originalName);
    }
});

// Initialize multer with the defined storage
const upload = multer({ storage: storage });

// Ensure the 'uploads' folder exists (create it if it doesn't)
const uploadsDir = path.join(__dirname, 'uploads');
if (!fs.existsSync(uploadsDir)) {
    fs.mkdirSync(uploadsDir);
}

// Route to handle file uploads from upload.html
app.post('/upload_handler', upload.any(), (req, res) => {
    console.log('Files uploaded:', req.files);

    // Redirect to thankyou.html after file upload
    res.redirect('/thankyou.html');
});

// Route to serve thankyou.html
app.get('/thankyou.html', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'thankyou.html'));
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
