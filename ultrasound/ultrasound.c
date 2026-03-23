#include <linux/module.h>
#include <linux/platform_device.h>
#include <linux/gpio/consumer.h>
#include <linux/delay.h>
#include <linux/slab.h>
#include <linux/uaccess.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/fs.h>
#include <linux/mod_devicetable.h>


MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Ultrasound distance sensor driver");
MODULE_AUTHOR("Joseph Joud");
MODULE_VERSION("1.0");
//MODULE_SUPPORTED_DEVICE("HC-SR04");

static ssize_t dev_read(struct file *,char *,size_t, loff_t *);
static int dev_open(struct inode *,struct file *);
static int dev_release(struct inode *,struct file *);
static int probe ( struct platform_device * pdev );

static struct file_operations fops = {
    .open = dev_open,
    .read = dev_read,
    .release = dev_release,
};

static const struct of_device_id ultrasound_dt[] = {
    { .compatible = "insa,ultrasound" }, // DOIT être identique au .dts
    {}                   // Toujours finir par un élément vide
};

static struct platform_driver ultrasound_driver = {
    .driver = {
        .name = "ultrasound",
        .of_match_table = ultrasound_dt, // Lien avec le Device Tree
    },
    .probe  = probe,  // Le probe est ici !
    .remove = NULL, //TODO
};


struct gpios {
    struct gpio_desc *trig_gpio;
    struct gpio_desc *echo_gpio;
};



struct device *dev;
struct gpios *us_gpios;
static int busy;
static int done;
static int major;

static int kinit ( void ) {
    /* register as a character device */
    major = register_chrdev (0 , "DUsound" , &fops );

    if (major < 0) {
        printk(KERN_ALERT "Ultrasound failed to register a major number\n");
        return major;
    }
    printk(KERN_INFO "Ultrasound: registered correctly with major number %d\n", major);
    
    done = busy = 0;
    
    return 0;
}

static void kexit ( void ) {
    unregister_chrdev ( major , "DUsound" ) ;
    return;
}

static int probe ( struct platform_device * pdev ) {

    dev = &pdev->dev; //ponter to device structure

    us_gpios = devm_kzalloc ( dev , sizeof ( struct gpios ) , GFP_KERNEL ) ;
    if ( !us_gpios ) {
        dev_err ( dev , "Failed to allocate memory for gpios\n" ) ;
        return -ENOMEM ;
    }
    us_gpios->trig_gpio = devm_gpiod_get ( dev , "trig" , GPIOD_OUT_LOW ) ;
    if ( IS_ERR ( us_gpios->trig_gpio ) ) {
        dev_err ( dev , "Failed to get trig gpio\n" ) ;
        return PTR_ERR ( us_gpios->trig_gpio ) ;
    }
    us_gpios->echo_gpio = devm_gpiod_get ( dev , "echo" , GPIOD_IN ) ;
    if ( IS_ERR ( us_gpios->echo_gpio ) ) {
        dev_err ( dev , "Failed to get echo gpio\n" ) ;
        return PTR_ERR ( us_gpios->echo_gpio ) ;
    }

    printk(KERN_INFO "Ultrasound: device probed\n");
}

static int dev_open ( struct inode * ino , struct file * fp ) {
/* if device is in use , reply with busy error */
    if ( busy ){
        return -EBUSY ;
    }   
    busy = 1; /* toggle device as busy */
    try_module_get ( THIS_MODULE ) ; /* tell the system that we’re live */
    return 0;
}

static int dev_release ( struct inode * ino , struct file * fp ) {
    busy = 0; /* toggle device as not busy */
    module_put ( THIS_MODULE ) ; /* tell the system that we’re done */
    return 0;
}

static ssize_t dev_read ( struct file * fp , char * buf , size_t n , loff_t * of )
{
    int result = 0;
    int distance = 0;
    int i;

    //send trigger 
    gpiod_set_value(us_gpios->trig_gpio,1);
    udelay(10);
    gpiod_set_value(us_gpios->trig_gpio,0);

    // wait for echo
    //TODO: add timeout
    //TODO: use passive wait

    while ( gpiod_get_value ( us_gpios->echo_gpio ) == 0 ) ;
    /* measure echo duration */
    for ( i = 0 ; i < 1000000 ; i++ ) {
        if ( gpiod_get_value ( us_gpios->echo_gpio ) == 0 ) {
            break;
        }
        udelay (1) ;
    }
    result = i;
    distance = result * 0.34 / 2; /* calculate distance in mm */
    

    if (copy_to_user(buf, &result, sizeof(result))) {
        return -EFAULT;
    } 

    /* copy data to user buffer */
    if ( copy_to_user ( buf , &result , sizeof ( result ) ) ) {
        return -EFAULT;
    }
    return sizeof ( result );
}

module_init(kinit);
module_exit(kexit);
