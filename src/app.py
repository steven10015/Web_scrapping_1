import sys
from service.tesla_revenue_service import TeslaRevenueService



def main():
    
    """Main function."""

    TeslaRevenueService().get_tesla_revenue()


if __name__ == "__main__":
    main()
    sys.exit(0)