<!DOCTYPE html>
<html>
<head>
  
</head>
<body>
    <h1>V2Ray Python API</h1>
    <p>This is a Python API for V2Ray that allows users to create and delete V2Ray accounts programmatically. It provides an easy-to-use interface that allows developers to automate the process of creating and deleting accounts.</p>
    <h2>Requirements</h2>
    <ul>
        <li>Python 3.x</li>
        <li><code>requests</code> module</li>
    </ul>
    <h2>Usage</h2>
    <h3>Creating an account</h3>
    <p>To create a new V2Ray account, instantiate the <code>V2Ray</code> class and call the <code>create_account</code> method with the following parameters:</p>
    <ul>
        <li><code>protocol</code>: string, must be either <code>'vmess'</code> or <code>'vless'</code></li>
        <li><code>remark</code>: string, the name of the account</li>
        <li><code>total</code>: integer, the total amount of data that the account is allowed to use (in GB)</li>
        <li><code>expire</code>: integer, the number of days until the account expires</li>
        <li><code>port</code>: integer (optional), the port number to use for incoming connections (default is a random port between 11111 and 55555)</li>
        <li><code>alert_id</code>: integer (optional), the alert ID to use for the account (default is 1)</li>
    </ul>
    <pre><code>from v2ray import V2Ray
v2ray = V2Ray('localhost', '8080', 'session_token')

result = v2ray.create_account('vmess', 'My V2Ray Account', 10, 30)
if result:
    print(result)
else:
    print('Failed to create account')</code></pre>
<h3>Deleting an account</h3>
<p>To delete a V2Ray account, call the <code>delete_account</code> method with one of the following parameters:</p>
<ul>
<li><code>by</code>: string, the name of the account to delete</li>
</ul>
<pre><code>from v2ray import V2Ray

v2ray = V2Ray('localhost', '8080', 'session_token')

result = v2ray.delete_account('My V2Ray Account')
if result:
    print(result)
else:
    print('Failed to delete account')</code></pre>
<h2>License</h2>
<p>This code is licensed under the <a href="https://opensource.org/licenses/MIT">MIT License</a>. Feel free to use it in your own projects or modify it to suit your needs.</p>
</body>
</html>
