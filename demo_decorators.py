from patterns.Factory_InstrumentTypes import Stock
from patterns.Decorators_Analytics import VolatilityDecorator, BetaDecorator, DrawdownDecorator


def main():
    # Create a simple Stock instrument (we don't modify the base class)
    stock = Stock({'symbol': 'AAPL', 'price': 169.89, 'type': 'stock'})

    # Stack decorators: volatility -> beta -> drawdown
    decorated = DrawdownDecorator(BetaDecorator(VolatilityDecorator(stock)))

    metrics = decorated.get_metrics()
    print(f"Metrics for {stock.symbol}:")
    for k, v in metrics.items():
        print(f"  {k}: {v}")


if __name__ == '__main__':
    main()
