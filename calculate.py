import click
import numpy as np


@click.command()
@click.option(
    "--order-size", "-s", type=float, prompt=True, help="Total size of all orders."
)
@click.option(
    "--num-orders", "-n", type=int, prompt=True, help="Number of orders to generate."
)
@click.option(
    "--lower-bound", type=float, prompt=True, help="Lower bound of order price."
)
@click.option(
    "--upper-bound", type=float, prompt=True, help="Upper bound of order price."
)
@click.option(
    "--order-type",
    type=click.Choice(["buy", "sell"], case_sensitive=False),
    prompt=True,
    help="Type of orders: 'buy' or 'sell'.",
)
@click.option(
    "--variance",
    "-v",
    type=float,
    default=0.2,
    prompt=True,
    help="Variance of order sizes.",
)
def calculate_orders(
    order_size, num_orders, lower_bound, upper_bound, order_type, variance
):
    if num_orders <= 0:
        raise click.BadParameter("Number of orders must be greater than 0")
    if lower_bound == upper_bound:
        raise click.BadParameter("Lower bound must not be equal to upper bound")
    if order_size <= 0:
        raise click.BadParameter("Total order size must be greater than 0")

    # Calculate order sizes from a linear function with bounded difference
    min_order_size = 1 - variance
    max_order_size = 1 + variance

    if order_type.lower() == "sell":
        order_prices = np.linspace(lower_bound, upper_bound, num_orders)
        order_sizes = np.linspace(min_order_size, max_order_size, num_orders)
    else:  # buy orders
        order_prices = np.linspace(upper_bound, lower_bound, num_orders)
        order_sizes = np.linspace(min_order_size, max_order_size, num_orders)

    # Normalize order sizes to match the total_order_size
    order_sizes = order_sizes / order_sizes.sum() * order_size

    order_sizes = np.round(order_sizes, 0)

    click.echo(click.style("\nOrders:", fg="green"))
    orders = list(zip(order_sizes, order_prices))

    for i, order in enumerate(orders, start=1):
        click.echo(
            click.style(
                f"Order {i}: Size = {order[0]:.2f}, Price = {order[1]:.2f}", fg="yellow"
            )
        )

    avg_order_size = sum(order[0] for order in orders) / num_orders
    avg_cost_price = sum(order[0] * order[1] for order in orders) / order_size
    click.echo(f"Average order size: {avg_order_size:.2f}")
    click.echo(f"Average cost price: {avg_cost_price:.2f}")


if __name__ == "__main__":
    calculate_orders()
