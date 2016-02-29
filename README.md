# cvcTools
[![Travis CI](https://travis-ci.org/soufiaane/CapValue.svg)](https://travis-ci.org/soufiaane/CapValue)
[![Circle CI](https://circleci.com/gh/soufiaane/CapValue.svg?style=shield)] (https://circleci.com/gh/soufiaane/CapValue)
[![Coverage Status](https://coveralls.io/repos/github/soufiaane/CapValue/badge.svg?branch=master)](https://coveralls.io/github/soufiaane/CapValue?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/grade/5bd087e2bf1644dda6f3af1b6bd00537)](https://www.codacy.com/app/mgh-soufiane/CapValue)

------------------------------------------
Requirements
------------------------------------------
python version =3.5.1 x64<br>
----------------


var io = require('socket.io')(3000);
var redis = require('redis').createClient;
var adapter = require('socket.io-redis');
var pub = redis(6379, 'localhost', { auth_pass: "cvc2016" });
var sub = redis(6379, 'localhost', { return_buffers: true, auth_pass: "cvc2016" });

io.adapter(adapter({ pubClient: pub, subClient: sub }));

io.sockets.on('connection', function(socket) {
  socket.on('message', function(data) {
   console.log(data);
  });
});
