def gradient_descent(learning_rate=0.1, max_iters=100):
    x = 0  # Initial guess
    for i in range(1, max_iters + 1):
        grad = 6 * x + 2  # Compute the gradient
        x = x - learning_rate * grad  # Update x
        
        if i % 100 == 0:  # Print every 100 iterations
            print(f"Iteration {i}: x = {x}")
    
    return x

x_min = gradient_descent()
print(f"Minimum occurs at x = {x_min}")
