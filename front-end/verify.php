 <?php
session_start();
require 'conn.php'; // Make sure you have the proper connection settings in this file.
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Email Verification & Password Reset - Questly</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
  <link rel="icon" href="ES.png" type="image/png">
<style>
    :root {
       --primary: #ff6b00;
            --primary-dark: #e06106ff;
            --secondary: #10b981;
            --dark: #1e293b;
            --light: #f2f2f2;
            --gray: #64748b;
            --error: #ef4444;
      --success: #22c55e;
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
      box-shadow: 0 2px 10px rgba(0,0,0,0.1);
      padding: 1rem 2rem;
      position: fixed;
      width: 100%;
      z-index: 100;
    }

    nav {
      display: flex;
      justify-content: space-between;
      align-items: center;
      max-width: 1200px;
      margin: 0 auto;
      flex-wrap: wrap;
    }

    .logo {
      display: flex;
      align-items: center;
      font-size: 1.8rem;
      font-weight: 700;
      color: var(--primary);
      text-decoration: none;
    }

    .logo span {
      color: var(--secondary);
    }

    main {
      margin-top: 100px; /* account for fixed header */
      padding: 2rem;
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
    }

    /* Styling for the form container */
    .form-container {
      width: 100%;
      max-width: 500px;
      margin: 0 auto;
      background-color: white;
      padding: 2.5rem;
      border-radius: 10px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
      transition: transform 0.3s ease;
    }

    .form-container:hover {
      transform: translateY(-5px);
    }

    .form-container h2 {
      font-size: 2rem;
      margin-bottom: 1.5rem;
      text-align: center;
      color: var(--dark);
    }

    .form-container form {
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
    }

    .form-group {
      position: relative;
    }

    .form-container input[type="number"],
    .form-container input[type="password"],
    .form-container input[type="text"],
    .form-container input[type="email"] {
      width: 100%;
      padding: 0.8rem 1rem;
      border: 1px solid #ddd;
      border-radius: 5px;
      font-size: 1rem;
      transition: border-color 0.3s;
    }

    .form-container input:focus {
      outline: none;
      border-color: var(--primary);
    }

    .form-container .input-icon {
      position: absolute;
      right: 1rem;
      top: 50%;
      transform: translateY(-50%);
      color: var(--gray);
    }

    .form-container .password-requirements {
      font-size: 0.85rem;
      color: var(--gray);
      margin-top: 0.5rem;
    }

    .form-container button[type="submit"],
    .form-container input[type="submit"] {
      width: 100%;
      padding: 0.8rem;
      background-color: var(--primary);
      border: none;
      border-radius: 5px;
      color: white;
      font-size: 1rem;
      font-weight: 500;
      cursor: pointer;
      transition: background 0.3s ease;
    }

    .form-container button[type="submit"]:hover,
    .form-container input[type="submit"]:hover {
      background-color: var(--primary-dark);
    }

    .message {
      text-align: center;
      margin-bottom: 1.5rem;
      padding: 1rem;
      border-radius: 5px;
      font-weight: 500;
    }

    .message.success {
      background-color: rgba(34, 197, 94, 0.1);
      color: var(--success);
      border: 1px solid rgba(34, 197, 94, 0.2);
    }

    .message.error {
      background-color: rgba(239, 68, 68, 0.1);
      color: var(--error);
      border: 1px solid rgba(239, 68, 68, 0.2);
    }

    .message.info {
      background-color: rgba(59, 130, 246, 0.1);
      color: var(--primary);
      border: 1px solid rgba(59, 130, 246, 0.2);
    }

    .go-back {
      display: flex;
      align-items: center;
      justify-content: center;
      margin-top: 1.5rem;
      text-decoration: none;
      color: var(--gray);
      font-weight: 500;
      gap: 0.5rem;
      transition: color 0.2s;
    }

    .go-back:hover {
      color: var(--primary);
    }

    .logo-container {
      text-align: center;
      margin-bottom: 1.5rem;
    }

    .status-icon {
      font-size: 3rem;
      margin-bottom: 1rem;
      text-align: center;
    }

    .success-icon {
      color: var(--success);
    }

    .error-icon {
      color: var(--error);
    }
.mainche{
                   padding-right:130px;
                }
    /* Responsive adjustments */
    @media (max-width: 768px) {
      .form-container {
        padding: 2rem 1.5rem;
      }
      
      .form-container h2 {
        font-size: 1.5rem;
      }
    }
  </style>
</head>
<body>
  <header>
    <nav>
  <div class="mainche">
                    <h1 style="font-size: 2rem;">
                      <a href="index.html" style="text-decoration: none; color: #ff6b00;">Questly</a>
                    </div>    </nav>
  </header>

  <main>
    <?php
      // Function to show message with proper styling
      function showMessage($text, $type = 'info') {
        return '<div class="message ' . $type . '">' . $text . '</div>';
      }

      // Display Email Verification Form if no reset token is provided via GET parameters.
      if (!isset($_GET['email']) && !isset($_GET['token'])) {
    ?>
        <div class="form-container">
          <div class="logo-container">
  <div class="mainche">
                    <h1 style="padding-left: 124px;font-size: 2rem;">
                      <a href="index.html" style="text-decoration: none; color: #ff6b00;">Questly</a>
                    </div>          </div>
          <div class="inner">
          <h2>Email Verification</h2>
          <?php
            // Optionally display any messages
            if (isset($message)) {
              echo showMessage($message);
            }
          ?>
          <form action="verify.php" method="post">
            <div class="form-group">
              <input type="number" name="verification_code" placeholder="Enter the code from your email" required>
              <i class="fas fa-key input-icon"></i>
            </div>
            <button type="submit" name="verify_email">Verify Email</button>
          </form>
          <a href="register.php" class="go-back">
            <i class="fas fa-arrow-left"></i> Back to Registration
          </a>
          <a class="go-back" href="https://mail.google.com/">Your verification code will be on your mail</a>
          </div>
        </div>
    <?php
      } else {
        $email = $_GET['email'];
        $token = $_GET['token'];

        // Check if the token is valid (using your provided logic)
        date_default_timezone_set('UTC');
        $current_date = date("Y-m-d");
        $query = "SELECT * FROM users WHERE email='$email' AND reset_token='$token' AND token_expiry = '$current_date'";
        $result = mysqli_query($conn, $query);

        if ($result && mysqli_num_rows($result) == 1) {
          ?>
          <div class="form-container">
            <div class="logo-container">
  <div class="mainche">
                    <h1 style="padding-left: 124px;font-size: 2rem;">
                      <a href="index.html" style="text-decoration: none; color: #ff6b00;">Questly</a>
                    </div>
                              </div>
            <h2>Reset Your Password</h2>
            <form action="password_reset.php" method="post">
              <input type="hidden" name="email" value="<?php echo htmlspecialchars($email); ?>">
              <input type="hidden" name="token" value="<?php echo htmlspecialchars($token); ?>">
              
              <div class="form-group">
                <input type="password" name="new_password" placeholder="New Password" required>
                <i class="fas fa-lock input-icon"></i>
                <div class="password-requirements">
                  Password must be at least 8 characters long
                </div>
              </div>
              
              <div class="form-group">
                <input type="password" name="confirm_password" placeholder="Confirm Password" required>
                <i class="fas fa-lock input-icon"></i>
              </div>
              
              <button type="submit" name="reset_password">Update Password</button>
            </form>
            <a href="login.php" class="go-back">
              <i class="fas fa-arrow-left"></i> Back to Login
            </a>
          </div>
          <?php
        } else {
          ?>
          <div class="form-container">
            <div class="logo-container">
  <div class="mainche">
                    <h1 style="padding-left: 124px;font-size: 2rem;">
                      <a href="index.html" style="text-decoration: none; color: #ff6b00;">Questly</a>
                    </div>            </div>
            <div class="status-icon error-icon">
              <i class="fas fa-times-circle"></i>
            </div>
            <?php echo showMessage('Invalid or expired reset token. Please request a new password reset link.', 'error'); ?>
            <a href="forgot_password.php" class="btn-primary" style="display: block; text-align: center; background-color: var(--primary); color: white; padding: 0.8rem; border-radius: 5px; text-decoration: none; font-weight: 500;">
              Request New Reset Link
            </a>
          </div>
          <?php
        }
      }

      // Process Email Verification Form Submission
      if (isset($_POST['verify_email'])) {
          $entered_code = $_POST['verification_code'];
          if ($_SESSION['register_pending']['code'] == $entered_code) {
              $username  = $_SESSION['register_pending']['username'];
              $full_name = $_SESSION['register_pending']['full_name'];
              $email     = $_SESSION['register_pending']['email'];
              $password  = $_SESSION['register_pending']['password'];
              
              $query = "INSERT INTO register_user (username, full_name, email, password) VALUES ('$username', '$full_name', '$email', '$password')";
              if (mysqli_query($conn, $query)) {
                  echo '<div class="form-container">';
                  echo '<div class="logo-container"><div class="mainche"><h1 style="padding-left: 124px;font-size: 2rem;"><a href="index.html" style="text-decoration: none; color: #ff6b00;">Questly</a></h1></div>';
                  echo '<div class="status-icon success-icon"><i class="fas fa-check-circle"></i></div>';
                  echo showMessage('Account verified successfully! You can now log in.', 'success');
                  echo '<a href="login.php" class="btn-primary" style="display: block; text-align: center; background-color: var(--primary); color: white; padding: 0.8rem; border-radius: 5px; text-decoration: none; font-weight: 500;">Log In Now</a>';
                  echo '</div>';
                  unset($_SESSION['register_pending']);


                  // Don't redirect immediately to allow user to see the success message
              } else {
                  echo '<div class="form-container">';
                  echo '<div class="logo-container"><div class="mainche"><h1 style="padding-left: 124px;font-size: 2rem;"><a href="index.html" style="text-decoration: none; color: #ff6b00;">Questly</a></h1></div>';
                  echo '<div class="status-icon error-icon"><i class="fas fa-times-circle"></i></div>';
                  echo showMessage('Your insrted code is invalide', 'error');
                  echo '<a href="register.php" class="btn-primary" style="display: block; text-align: center; background-color: var(--primary); color: white; padding: 0.8rem; border-radius: 5px; text-decoration: none; font-weight: 500;">Try Again</a>';
                  echo '</div>';

                  
              }
          } else {
              echo '<div class="form-container">';
              echo '<div class="logo-container"><div class="mainche"><h1 style="padding-left: 124px;font-size: 2rem;"><a href="index.html" style="text-decoration: none; color: #ff6b00;">Questly</a></h1></div>';
              echo '<div class="status-icon error-icon"><i class="fas fa-times-circle"></i></div>';
              echo showMessage('Invalid verification code! Please check your email and try again.', 'error');
              echo '<a href="javascript:history.back()" class="btn-primary" style="display: block; text-align: center; background-color: var(--primary); color: white; padding: 0.8rem; border-radius: 5px; text-decoration: none; font-weight: 500;">Try Again</a>';
              echo '</div>';
          }
      }

      // Process Password Reset Form Submission
      if (isset($_POST['reset_password'])) {
          echo '<div class="form-container">';
          echo '<div class="logo-container"><div class="mainche"><h1 style="padding-left: 124px;font-size: 2rem;"><a href="index.html" style="text-decoration: none; color: #ff6b00;">Questly</a></h1></div>';
          
          if ($_POST['new_password'] !== $_POST['confirm_password']) {
              echo '<div class="status-icon error-icon"><i class="fas fa-times-circle"></i></div>';
              echo showMessage('Passwords do not match! Please try again.', 'error');
              echo '<a href="javascript:history.back()" class="btn-primary" style="display: block; text-align: center; background-color: var(--primary); color: white; padding: 0.8rem; border-radius: 5px; text-decoration: none; font-weight: 500;">Try Again</a>';
          } else {
              $hashed_password = hash('sha256', $_POST['new_password']);
              $email = $_POST['email'];
              
              if (filter_var($email, FILTER_VALIDATE_EMAIL)) {
                  $email_domain = substr(strrchr($email, "@"), 1);
                  if ($email_domain !== "mail.ljku.edu.in") {
                      echo '<div class="status-icon error-icon"><i class="fas fa-times-circle"></i></div>';
                      echo showMessage('Only \'@mail.ljku.edu.in\' emails are allowed!', 'error');
                      echo '<a href="login.php" class="btn-primary" style="display: block; text-align: center; background-color: var(--primary); color: white; padding: 0.8rem; border-radius: 5px; text-decoration: none; font-weight: 500;">Back to Login</a>';
                  } else {
                      $update = "UPDATE users SET password='$hashed_password', reset_token=NULL, token_expiry=NULL WHERE email='$email'";
                      if (mysqli_query($conn, $update)) {
                          echo '<div class="status-icon success-icon"><i class="fas fa-check-circle"></i></div>';
                          echo showMessage('Password reset successful! You can now log in with your new password.', 'success');
                          echo '<a href="login.php" class="btn-primary" style="display: block; text-align: center; background-color: var(--primary); color: white; padding: 0.8rem; border-radius: 5px; text-decoration: none; font-weight: 500;">Log In Now</a>';
                      } else {
                          echo '<div class="status-icon error-icon"><i class="fas fa-times-circle"></i></div>';
                          echo showMessage('Failed to reset password: ' . mysqli_error($conn), 'error');
                          echo '<a href="javascript:history.back()" class="btn-primary" style="display: block; text-align: center; background-color: var(--primary); color: white; padding: 0.8rem; border-radius: 5px; text-decoration: none; font-weight: 500;">Try Again</a>';
                      }
                  }
              } else {
                  echo '<div class="status-icon error-icon"><i class="fas fa-times-circle"></i></div>';
                  echo showMessage('Invalid email format!', 'error');
                  echo '<a href="login.php" class="btn-primary" style="display: block; text-align: center; background-color: var(--primary); color: white; padding: 0.8rem; border-radius: 5px; text-decoration: none; font-weight: 500;">Back to Login</a>';
              }
          }
          echo '</div>';
      }
    ?>
  </main>
</body>
</html