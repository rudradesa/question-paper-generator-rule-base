 <?php
require('conn.php');
if (isset($_GET['email']) && isset($_GET['reset_token'])) {
    date_default_timezone_set('Asia/Kolkata');
    $data = date("Y-m-d");
    $email = $_GET['email'];
    $reset_token = $_GET['reset_token'];
    $query = "SELECT * FROM register_user WHERE email='$email' AND resettoken='$reset_token' AND resettokenexp = '$data'";
    $result = mysqli_query($conn, $query);
    if ($result && mysqli_num_rows($result) == 1) {
        ?>
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
            <title>Reset Password - Questly</title>
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
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }

                body {
                    background-color: var(--light);
                    color: var(--dark);
                    line-height: 1.6;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    padding: 2rem;
                }

                .reset-container {
                    background-color: white;
                    border-radius: 10px;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                    padding: 2.5rem;
                    width: 100%;
                    max-width: 500px;
                    text-align: center;
                }

                .logo {
                    font-size: 2rem;
                    font-weight: 700;
                    color: var(--primary);
                    margin-bottom: 1.5rem;
                }

                .logo span {
                    color: var(--secondary);
                }

                h2 {
                    font-size: 1.8rem;
                    margin-bottom: 1.5rem;
                    color: var(--dark);
                }

                .form-group {
                    margin-bottom: 1.5rem;
                }

                input[type="password"] {
                    width: 100%;
                    padding: 0.8rem 1rem;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    font-size: 1rem;
                    transition: border-color 0.3s;
                }

                input[type="password"]:focus {
                    outline: none;
                    border-color: var(--primary);
                }

                .password-requirements {
                    text-align: left;
                    font-size: 0.85rem;
                    color: var(--gray);
                    margin-top: 0.5rem;
                }

                .btn {
                    background-color: var(--primary);
                    color: white;
                    border: none;
                    padding: 0.8rem 2rem;
                    border-radius: 5px;
                    font-size: 1rem;
                    font-weight: 500;
                    cursor: pointer;
                    transition: background-color 0.3s;
                    width: 100%;
                }

                .btn:hover {
                    background-color: var(--primary-dark);
                }

                .back-link {
                    display: inline-block;
                    margin-top: 1.5rem;
                    color: var(--primary);
                    text-decoration: none;
                    font-weight: 500;
                }

                .back-link:hover {
                    text-decoration: underline;
                }
                .mainche{
                   padding-right:150px;
                }
                @media (max-width: 768px) {
                    .reset-container {
                        padding: 2rem 1.5rem;
                    }
                }
            </style>
            <link rel="icon" href="ES.png" type="image/png">
        </head>
        <body>
            <div class="reset-container">
                <div class="mainche">
                    <h1 style="padding-left: 124px;font-size: 2rem;">
                      <a href="index.html" style="text-decoration: none; color: #ff6b00;">Questly</a>
                    </div>
                </h1>                <h2>Reset Your Password</h2>
                    
                <form action="reset-password.php" method="post">
                    <input type="hidden" name="email" value="<?php echo htmlspecialchars($email); ?>">
                    <input type="hidden" name="reset_token" value="<?php echo htmlspecialchars($reset_token); ?>">
                    
                    <div class="form-group">
                        <input type="password" name="new_password" placeholder="New Password" required>
                        <div class="password-requirements">
                            Password must be at least 8 characters long
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <input type="password" name="confirm_password" placeholder="Confirm Password" required>
                    </div>
                    
                    <button type="submit" class="btn" name="update_password">Update Password</button>
                </form>
                <a href="login.php" class="back-link">Back to Login</a>
            </div>
        </body>
        </html>
        <?php
    } else {
        ?>
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
            <title>Invalid Token - Questly</title>
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
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    padding: 2rem;
                }

                .error-container {
                    background-color: white;
                    border-radius: 10px;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                    padding: 2.5rem;
                    width: 100%;
                    max-width: 500px;
                    text-align: center;
                }

                .logo {
                    font-size: 2rem;
                    font-weight: 700;
                    color: var(--primary);
                    margin-bottom: 1.5rem;
                }

                .logo span {
                    color: var(--secondary);
                }

                .error-icon {
                    font-size: 3rem;
                    color: var(--error);
                    margin-bottom: 1rem;
                }

                .error-message {
                    font-size: 1.2rem;
                    margin-bottom: 1.5rem;
                    color: var(--dark);
                }

                .btn {
                    background-color: var(--primary);
                    color: white;
                    border: none;
                    padding: 0.8rem 2rem;
                    border-radius: 5px;
                    font-size: 1rem;
                    font-weight: 500;
                    cursor: pointer;
                    transition: background-color 0.3s;
                    text-decoration: none;
                    display: inline-block;
                }
.mainche{
                   padding-right:150px;
                }
                .btn:hover {
                    background-color: var(--primary-dark);
                }
            </style>
        </head>
        <body>
            <div class="error-container">
                  <div class="mainche">
                    <h1 style="padding-left: 124px;font-size: 2rem;">
                      <a href="index.html" style="text-decoration: none; color: #ff6b00;">Questly</a>
                    </div>
                <div class="error-icon">❌</div>
                <p class="error-message">Invalid or expired password reset token.</p>
                <a href="forgot-password.php" class="btn">Request New Reset Link</a>
            </div>
        </body>
        </html>
        <?php
    }
}

if (isset($_POST['update_password'])) {
    // Create a response page
    ?>
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <title>Password Reset - Questly</title>
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
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }

            body {
                background-color: var(--light);
                color: var(--dark);
                line-height: 1.6;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                padding: 2rem;
            }

            .response-container {
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                padding: 2.5rem;
                width: 100%;
                max-width: 500px;
                text-align: center;
            }

            .logo {
                font-size: 2rem;
                font-weight: 700;
                color: var(--primary);
                margin-bottom: 1.5rem;
            }

            .logo span {
                color: var(--secondary);
            }

            .status-icon {
                font-size: 3rem;
                margin-bottom: 1rem;
            }

            .success-icon {
                color: var(--success);
            }

            .error-icon {
                color: var(--error);
            }

            .response-message {
                font-size: 1.2rem;
                margin-bottom: 1.5rem;
                color: var(--dark);
            }

            .btn {
                background-color: var(--primary);
                color: white;
                border: none;
                padding: 0.8rem 2rem;
                border-radius: 5px;
                font-size: 1rem;
                font-weight: 500;
                cursor: pointer;
                transition: background-color 0.3s;
                text-decoration: none;
                display: inline-block;
            }

            .btn:hover {
                background-color: var(--primary-dark);
            }
            .mainche{
                   padding-right:120px;
                }
        </style>
    </head>
    <body>
        <div class="response-container">
  <div class="mainche">
                    <h1 style="padding-left: 124px;font-size: 2rem;">
                      <a href="index.html" style="text-decoration: none; color: #ff6b00;">Questly</a>
                    </div>            <?php
           
            if ($_POST['new_password'] !== $_POST['confirm_password']) {
                echo '<div class="status-icon error-icon">❌</div>';
                echo '<p class="response-message">Passwords do not match!</p>';
                echo '<a href="javascript:history.back()" class="btn">Try Again</a>';
            } else {
                
                $pass = hash('sha256', $_POST['new_password']);
                $email = $_POST['email'];
                
                
                if (filter_var($email, FILTER_VALIDATE_EMAIL)) {
                   
                        
                        $update = "UPDATE register_user SET Password='$pass', resettoken=NULL, resettokenexp=NULL WHERE email='$email'";
                        if (mysqli_query($conn, $update)) {
                            echo '<div class="status-icon success-icon">✅</div>';
                            echo '<p class="response-message">Password updated successfully!</p>';
                            echo '<a href="login.php" class="btn">Log In Now</a>';
                        } else {
                            echo '<div class="status-icon error-icon">❌</div>';
                            echo '<p class="response-message">Failed to update password: ' . mysqli_error($conn) . '</p>';
                            echo '<a href="javascript:history.back()" class="btn">Try Again</a>';
                        }
                    
                } else {
                    echo '<div class="status-icon error-icon">❌</div>';
                    echo '<p class="response-message">Invalid email format!</p>';
                    echo '<a href="login.php" class="btn">Back to Login</a>';
                }
            }
            ?>
        </div>
    </body>
    </html>
    <?php
    exit();
}
?>