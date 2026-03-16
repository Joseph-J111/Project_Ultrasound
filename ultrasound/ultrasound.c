#include <linux/module.h>
#include <linux/platform_device.h>
#include <linux/gpio/consumer.h>
#include <linux/delay.h>
#include <linux/slab.h>

struct ultrasound_data {
    struct gpio_desc *trigger;
    struct gpio_desc *echo;
};

/* --- Fonctions Driver --- */

static int ultrasound_probe(struct platform_device *pdev) {
    struct ultrasound_data *data;
    struct device *dev = &pdev->dev;

    data = devm_kzalloc(dev, sizeof(struct ultrasound_data), GFP_KERNEL);
    if (!data) return -ENOMEM;

    data->trigger = devm_gpiod_get(dev, "trigger", GPIOD_OUT_LOW);
    data->echo = devm_gpiod_get(dev, "echo", GPIOD_IN);

    if (IS_ERR(data->trigger) || IS_ERR(data->echo)) {
        dev_err(dev, "Erreur lors de la récupération des GPIOs\n");
        return -1;
    }

    /* Test Trigger au chargement */
    gpiod_set_value(data->trigger, 1);
    udelay(10);
    gpiod_set_value(data->trigger, 0);

    dev_info(dev, "Ultrasound Probe : Matériel détecté et Trigger envoyé !\n");
    platform_set_drvdata(pdev, data);
    return 0;
}

static int ultrasound_remove(struct platform_device *pdev) {
    dev_info(&pdev->dev, "Ultrasound Remove : Nettoyage du matériel\n");
    return 0;
}

/* --- Liaison Device Tree --- */

static const struct of_device_id ultrasound_dt_ids[] = {
    { .compatible = "insa,ultrasound", },
    { }
};

static struct platform_driver ultrasound_driver = {
    .driver = {
        .name = "ultrasound_insa",
        .of_match_table = ultrasound_dt_ids,
    },
    .probe = ultrasound_probe,
    .remove = ultrasound_remove,
};

/* --- Fonctions INIT / EXIT que tu souhaites garder --- */

static int __init ultrasound_module_init(void) {
    pr_info("--- Début de l'installation du module Ultrasound ---\n");
    // On enregistre le driver auprès du noyau
    return platform_driver_register(&ultrasound_driver);
}

static void __exit ultrasound_module_exit(void) {
    pr_info("--- Sortie du module Ultrasound ---\n");
    // On désenregistre le driver
    platform_driver_unregister(&ultrasound_driver);
}

module_init(ultrasound_module_init);
module_exit(ultrasound_module_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Insa");
