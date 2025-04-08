import numpy as np

def gradient_descent(gradient, start, learning_rate=0.1, n_iter=100, tol=1e-6):
    """
    Perform Gradient Descent to minimize a function.

    Parameters:
        gradient (function): The gradient function of the objective function.
        start (float): The initial point to start the optimization.
        learning_rate (float): The step size for each iteration.
        n_iter (int): The maximum number of iterations.
        tol (float): The tolerance for stopping criteria.

    Returns:
        float: The optimized value of x.
    """
    x = start  # Initialize the starting point
    for _ in range(n_iter):
        grad = gradient(x)  # Compute the gradient at the current point
        if np.abs(grad) < tol:  # Check if the gradient is close to zero (stopping condition)
            break
        x = x - learning_rate * grad  # Update x using the gradient
    return x

# Define the objective function and its gradient
def f(x):
    return 3* x**2 + 2 *x + 1  # Example function: f(x) = 3x^2 + 2x + 1 

def grad_f(x):
    return 6 * x + 2 # Gradient of f(x): f'(x) = 6x + 2

# Run Gradient Descent
start = 10.0  # Initial point
solution = gradient_descent(grad_f, start)
print("Solution found:", solution)