const http = require('http');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const server = http.createServer((req, res) => {
    if (req.method === 'GET' && req.url === '/') {
        fs.readFile(path.join(__dirname, 'index.html'), 'utf8', (err, data) => {
            if (err) {
                res.writeHead(500, { 'Content-Type': 'text/plain' });
                res.end('500 Internal Server Error');
                return;
            }
            res.writeHead(200, { 'Content-Type': 'text/html' });
            res.end(data);
        });
    } else if (req.method === 'POST' && req.url === '/run-script') {
        let body = '';
        req.on('data', chunk => {
            body += chunk.toString();
        });
        req.on('end', () => {
            const inputData = JSON.parse(body);
            const childPython = spawn('python', ['Random_büyüklük.py', JSON.stringify(inputData)]);

            childPython.on('close', (code) => {
                console.log(`Python script exited with code ${code}`);
                
                // Wait for 3 seconds
                setTimeout(() => {
                    // Read the tahmin_sonucu.txt file
                    fs.readFile('tahmin_sonucu.txt', 'utf8', (err, data) => {
                        if (err) {
                            res.writeHead(500, { 'Content-Type': 'text/plain' });
                            res.end('500 Internal Server Error');
                            return;
                        }
                        res.writeHead(200, { 'Content-Type': 'application/json' });
                        res.end(JSON.stringify({ prediction: data.trim() }));
                    });
                },0);
            });

            childPython.stderr.on('data', (data) => {
                console.error(`stderr: ${data}`);
            });
        });
    } else {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('404 Not Found');
    }
});

server.listen(5000, () => {
    console.log('Server is running on http://localhost:5000');
});
