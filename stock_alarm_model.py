import pandas as pd
from datetime import datetime, timedelta

class StockAlarmSystem:
    def __init__(self, data_file):
        """Initialize the stock monitoring system"""
        self.df = pd.read_csv(data_file)
        self.today = datetime.now()
        
    def analyze_stock_levels(self):
        """Analyze current stock levels and identify items needing attention"""
        critical_items = []
        warning_items = []
        reorder_items = []
        
        for _, item in self.df.iterrows():
            days_of_stock = item['current_stock'] / item['avg_daily_sales'] if item['avg_daily_sales'] > 0 else float('inf')
            
            # Calculate reorder point considering lead time
            reorder_point = item['minimum_stock'] + (item['avg_daily_sales'] * item['lead_time_days'])
            
            status = {
                'product_id': item['product_id'],
                'category': item['category'],
                'item_name': item['item_name'],
                'current_stock': item['current_stock'],
                'minimum_stock': item['minimum_stock'],
                'days_of_stock': round(days_of_stock, 1),
                'lead_time_days': item['lead_time_days'],
                'reorder_quantity': item['maximum_stock'] - item['current_stock']
            }
            
            if item['current_stock'] <= item['minimum_stock']:
                critical_items.append(status)
            elif item['current_stock'] <= reorder_point:
                warning_items.append(status)
            elif item['current_stock'] <= item['maximum_stock'] * 0.7:
                reorder_items.append(status)
                
        return critical_items, warning_items, reorder_items
    
    def generate_report(self):
        """Generate a comprehensive stock status report"""
        critical, warning, reorder = self.analyze_stock_levels()
        
        report = f"Stock Status Report - {self.today.strftime('%Y-%m-%d %H:%M')}\n\n"
        
        if critical:
            report += "CRITICAL - IMMEDIATE ACTION REQUIRED!\n"
            report += "===================================\n"
            for item in critical:
                report += self._format_item_report(item, "CRITICAL")
        
        if warning:
            report += "\nWARNING - Order Soon\n"
            report += "===================\n"
            for item in warning:
                report += self._format_item_report(item, "WARNING")
        
        if reorder:
            report += "\nConsider Reordering\n"
            report += "===================\n"
            for item in reorder:
                report += self._format_item_report(item, "REORDER")
        
        return report
    
    def _format_item_report(self, item, level):
        """Format individual item report"""
        report = f"{item['category']} - {item['item_name']} (ID: {item['product_id']})\n"
        report += f"  Current Stock: {item['current_stock']} units\n"
        report += f"  Minimum Stock: {item['minimum_stock']} units\n"
        report += f"  Days of Stock Remaining: {item['days_of_stock']} days\n"
        report += f"  Suggested Order Quantity: {item['reorder_quantity']} units\n"
        if level == "CRITICAL":
            report += "  ⚠️ STOCK OUT RISK - Order Immediately!\n"
        report += "\n"
        return report
    
    def get_summary_stats(self):
        """Get summary statistics of inventory status"""
        critical, warning, reorder = self.analyze_stock_levels()
        total_items = len(self.df)
        
        stats = {
            'total_products': total_items,
            'critical_items': len(critical),
            'warning_items': len(warning),
            'reorder_items': len(reorder),
            'healthy_items': total_items - len(critical) - len(warning) - len(reorder),
            'critical_categories': len(set(item['category'] for item in critical)),
            'total_categories': len(self.df['category'].unique())
        }
        return stats

# Usage Example
if __name__ == "__main__":
    # Initialize system
    system = StockAlarmSystem('local_store_inventory.csv')
    
    # Generate and print report
    print(system.generate_report())
    
    # Print summary statistics
    stats = system.get_summary_stats()
    print("\nInventory Summary:")
    print(f"Total Products: {stats['total_products']}")
    print(f"Critical Items: {stats['critical_items']}")
    print(f"Warning Items: {stats['warning_items']}")
    print(f"Items to Reorder: {stats['reorder_items']}")
    print(f"Healthy Items: {stats['healthy_items']}")