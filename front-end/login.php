 <?php
    
?><!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Questly</title>
</head>
<body>
    <header>
      
    
<h1 style="padding-left: 124px;font-size: 2rem;">
  <a href="index.html" style="text-decoration: none; color: #ff6b00;">Questly</a>
</h1>

    </header>

    <div class="login-container">
        <div class="login-card">
            <div class="login-header">
                <h1>Welcome Back</h1>
                <p>Log in to make paper</p>
            </div>
            
            <div class="error-message" id="errorMessage"></div>
            
            <?php
            require('conn.php');
            session_start();
            if (isset($_POST['login'])) {
                $email = isset($_POST['email']) ? trim($_POST['email']) : '';
                $password = isset($_POST['password']) ? trim($_POST['password']) : '';

                if (empty($email) || empty($password)) {
                    echo "<script>
                        document.getElementById('errorMessage').style.display = 'block';
                        document.getElementById('errorMessage').textContent = '❌ Email or Password is missing!';
                    </script>";
                    exit;
                }


              


                $query = "SELECT * FROM register_user WHERE email = '$email'";
                $result = mysqli_query($conn, $query);

                if ($result && mysqli_num_rows($result) == 1) {
                    $row = mysqli_fetch_assoc($result);
                    $hashed_input_password = hash('sha256', $password);

                    if ($hashed_input_password === $row['password']) {
                        $_SESSION['user_id'] = $row['user_id'];
                        $_SESSION['username'] = $row['username'];
                        $_SESSION['email'] = $row['email'];
                        header("Location:http://127.0.0.1:5000");
                        exit;
                    } else {
                        echo "<script>
                            document.getElementById('errorMessage').style.display = 'block';
                            document.getElementById('errorMessage').textContent = '❌ Invalid password!';
                        </script>";
                    }
                } else {
                    echo "<script>
                        document.getElementById('errorMessage').style.display = 'block';
                        document.getElementById('errorMessage').textContent = '❌ User not found!';
                    </script>";
                }
            }
            ?>
            
            <form action="login.php" method="post">
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" placeholder="Email id" required>
                </div>
                
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" placeholder="Enter your password" required>
                </div>
                
                <button type="submit" name="login" class="submit-btn">Log In</button>
                
                <div class="form-links">
                    <a href="register.php">Create Account</a>
                    <a href="forgotpass.php">Forgot Password?</a>
                </div>
            </form>
            
            <a href="index.html" class="return-home">← Back to Home</a>
        </div>
    </div>

    <footer>
        <p>&copy; 2025 Questly. All rights reserved.</p>
    </footer>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const urlParams = new URLSearchParams(window.location.search);
            const error = urlParams.get('error');
            
            if (error) {
                const errorMessage = document.getElementById('errorMessage');
                errorMessage.style.display = 'block';
                errorMessage.textContent = decodeURIComponent(error);
            }
        });
    </script>
    <style>
        :root {
            --primary: #ff6b00;
            --primary-dark: #e06106ff;
            --secondary: #10b981;
            --dark: #1e293b;
            --light: #f2f2f2;
            --gray: #64748b;
            --error: #ef4444;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
                  font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;

        }
        
        body {
            background-color: var(--light);
            color: var(--dark);
            line-height: 1.6;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        header {
            background-color: white;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            padding: 1rem 2rem;
            width: 100%;
        }
        
        nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .logo {
            display: flex;
            align-items: center;
            font-size: 2rem;
            font-weight: 700;
            color: var(--primary);
            text-decoration: none;
        }
        
        .logo span {
            color: var(--secondary);
        }
        
        .login-container {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem;
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(16, 185, 129, 0.1));
        }
        
        .login-card {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 450px;
            padding: 2.5rem;
        }
        
        .login-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .login-header h1 {
            font-size: 2rem;
            color: var(--dark);
            margin-bottom: 0.5rem;
        }
        
        .login-header p {
            color: var(--gray);
        }
        
        .error-message {
            padding: 0.75rem;
            background-color: rgba(239, 68, 68, 0.1);
            color: var(--error);
            border-radius: 5px;
            margin-bottom: 1.5rem;
            display: none;
        }
        
        form {
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
            width: 100%;
        }
        
        .form-group {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }
        
        .form-group label {
            font-weight: 500;
            color: var(--dark);
        }
        
        .form-group input {
            padding: 0.75rem 1rem;
            border: 1px solid #e2e8f0;
            border-radius: 5px;
            font-size: 1rem;
            transition: border 0.3s;
        }
        
        .form-group input:focus {
            outline: none;
            border-color: var(--primary);
        }
        
        .submit-btn {
            background-color: var(--primary);
            color: white;
            border: none;
            padding: 0.75rem;
            font-size: 1rem;
            font-weight: 500;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        
        .submit-btn:hover {
            background-color: var(--primary-dark);
        }
        
        .form-links {
            display: flex;
            justify-content: space-between;
            margin-top: 1rem;
        }
        
        .form-links a {
            color: var(--primary);
            text-decoration: none;
            font-size: 0.9rem;
            transition: color 0.3s;
        }
        
        .form-links a:hover {
            color: var(--primary-dark);
            text-decoration: underline;
        }
        
        .return-home {
            display: block;
            text-align: center;
            margin-top: 2rem;
            color: var(--gray);
            text-decoration: none;
            font-size: 0.9rem;
        }
        
        .return-home:hover {
            color: var(--dark);
        }
        
        footer {
            background-color: var(--dark);
            color: white;
            padding: 1.5rem;
            text-align: center;
        }
        
        @media (max-width: 768px) {
            .login-card {
                padding: 1.5rem;
            }
        }
    </style>
</body>
</html