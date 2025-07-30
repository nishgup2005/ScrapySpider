# Define your item pipelines here
# OPTIMIZED VERSION - Significant performance improvements and monitoring

# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd
import time
import logging
import os
from scrapy.exceptions import DropItem

class PhhcCrawlerPipeline:
    """Basic pipeline for item validation and cleaning"""
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Basic validation - drop empty items
        if not any(adapter.values()):
            raise DropItem(f"Empty item found: {item!r}")
            
        # Clean up whitespace in text fields
        for key, value in adapter.items():
            if isinstance(value, str):
                adapter[key] = value.strip()
                
        return item

class PerformancePipeline:
    """Pipeline for monitoring scraping performance in real-time"""
    
    def __init__(self):
        self.item_count = 0
        self.start_time = time.time()
        self.last_report_time = time.time()
        self.last_report_count = 0
        self.report_interval = 100  # Report every 100 items
        
    def process_item(self, item, spider):
        self.item_count += 1
        current_time = time.time()
        
        # Report performance every N items
        if self.item_count % self.report_interval == 0:
            elapsed_time = current_time - self.start_time
            interval_time = current_time - self.last_report_time
            interval_items = self.item_count - self.last_report_count
            
            overall_rate = self.item_count / elapsed_time if elapsed_time > 0 else 0
            interval_rate = interval_items / interval_time if interval_time > 0 else 0
            
            spider.logger.info(
                f"Performance Update - Total Items: {self.item_count}, "
                f"Overall Rate: {overall_rate:.1f} items/sec, "
                f"Current Rate: {interval_rate:.1f} items/sec, "
                f"Elapsed Time: {elapsed_time/60:.1f} minutes"
            )
            
            self.last_report_time = current_time
            self.last_report_count = self.item_count
            
        return item
    
    def close_spider(self, spider):
        elapsed_time = time.time() - self.start_time
        final_rate = self.item_count / elapsed_time if elapsed_time > 0 else 0
        
        spider.logger.info(
            f"Final Performance Stats - Total Items: {self.item_count}, "
            f"Total Time: {elapsed_time/60:.1f} minutes, "
            f"Average Rate: {final_rate:.1f} items/sec"
        )

class OptimizedExcelExportPipeline:
    """Optimized pipeline for Excel export with memory management and error handling"""
    
    def __init__(self):
        self.items = []
        self.batch_size = 1000  # Process items in batches to manage memory
        self.batch_count = 0
        self.temp_files = []
        
    def process_item(self, item, spider):
        self.items.append(dict(item))
        
        # Process in batches to avoid memory issues
        if len(self.items) >= self.batch_size:
            self._save_batch(spider)
            
        return item
    
    def _save_batch(self, spider):
        """Save a batch of items to a temporary file"""
        if not self.items:
            return
            
        try:
            df = pd.DataFrame(self.items)
            temp_filename = f"temp_batch_{self.batch_count}.xlsx"
            df.to_excel(temp_filename, index=False)
            self.temp_files.append(temp_filename)
            self.batch_count += 1
            
            spider.logger.info(f"Saved batch {self.batch_count} with {len(self.items)} items")
            
            # Clear items to free memory
            self.items = []
            
        except Exception as e:
            spider.logger.error(f"Error saving batch {self.batch_count}: {e}")
    
    def close_spider(self, spider):
        """Combine all batches into final Excel file and clean up"""
        try:
            # Save any remaining items
            if self.items:
                self._save_batch(spider)
            
            if not self.temp_files:
                spider.logger.warning("No data to export")
                return
            
            # Combine all temporary files
            all_dataframes = []
            for temp_file in self.temp_files:
                try:
                    df = pd.read_excel(temp_file)
                    all_dataframes.append(df)
                except Exception as e:
                    spider.logger.error(f"Error reading {temp_file}: {e}")
            
            if all_dataframes:
                # Combine all dataframes
                final_df = pd.concat(all_dataframes, ignore_index=True)
                
                # Export to final Excel file with timestamp
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                final_filename = f"phhc_results_{timestamp}.xlsx"
                
                # Add some formatting and metadata
                with pd.ExcelWriter(final_filename, engine='openpyxl') as writer:
                    final_df.to_excel(writer, sheet_name='Case_Data', index=False)
                    
                    # Add summary sheet
                    summary_data = {
                        'Metric': ['Total Cases', 'Unique Case Types', 'Date Range', 'Export Time'],
                        'Value': [
                            len(final_df),
                            final_df['case_type'].nunique() if 'case_type' in final_df.columns else 'N/A',
                            f"{final_df['date'].min()} to {final_df['date'].max()}" if 'date' in final_df.columns else 'N/A',
                            time.strftime("%Y-%m-%d %H:%M:%S")
                        ]
                    }
                    summary_df = pd.DataFrame(summary_data)
                    summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                spider.logger.info(f"Successfully exported {len(final_df)} items to {final_filename}")
                
                # Clean up temporary files
                for temp_file in self.temp_files:
                    try:
                        os.remove(temp_file)
                    except Exception as e:
                        spider.logger.warning(f"Could not remove {temp_file}: {e}")
                        
            else:
                spider.logger.error("No valid data found in temporary files")
                
        except Exception as e:
            spider.logger.error(f"Error in close_spider: {e}")
            # Fallback: try to save whatever data we have
            if self.items:
                try:
                    df = pd.DataFrame(self.items)
                    df.to_excel("fallback_results.xlsx", index=False)
                    spider.logger.info(f"Saved {len(self.items)} items to fallback_results.xlsx")
                except Exception as fallback_error:
                    spider.logger.error(f"Fallback save also failed: {fallback_error}")

class DataValidationPipeline:
    """Pipeline for data quality validation and filtering"""
    
    def __init__(self):
        self.stats = {
            'total_items': 0,
            'valid_items': 0,
            'invalid_items': 0,
            'duplicate_items': 0
        }
        self.seen_items = set()
    
    def process_item(self, item, spider):
        self.stats['total_items'] += 1
        adapter = ItemAdapter(item)
        
        # Create a simple fingerprint for duplicate detection
        fingerprint = f"{adapter.get('case_number', '')}-{adapter.get('date', '')}-{adapter.get('case_type', '')}"
        
        if fingerprint in self.seen_items:
            self.stats['duplicate_items'] += 1
            spider.logger.debug(f"Duplicate item found: {fingerprint}")
            raise DropItem(f"Duplicate item: {fingerprint}")
        
        self.seen_items.add(fingerprint)
        
        # Validate required fields
        required_fields = ['case_number', 'date', 'case_type']
        missing_fields = [field for field in required_fields if not adapter.get(field)]
        
        if missing_fields:
            self.stats['invalid_items'] += 1
            spider.logger.warning(f"Item missing required fields {missing_fields}: {item}")
            raise DropItem(f"Missing required fields: {missing_fields}")
        
        self.stats['valid_items'] += 1
        return item
    
    def close_spider(self, spider):
        spider.logger.info(f"Data Validation Stats: {self.stats}")

# Legacy pipeline kept for backward compatibility
class ExcelExportPipeline:
    """Legacy pipeline - kept for backward compatibility, but OptimizedExcelExportPipeline is recommended"""
    
    def __init__(self):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item

    def close_spider(self, spider):
        if self.items:
            df = pd.DataFrame(self.items)
            df.to_excel("results.xlsx", index=False)
            spider.logger.info(f"Exported {len(self.items)} items to results.xlsx")