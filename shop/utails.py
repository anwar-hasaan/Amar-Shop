def get_upload_dir(instance, filename):
    return 'products/{0}'.format(filename)

DISTRICT_CHOICES = (
    ('dhaka', 'Dhaka'),
    ('gazipur', 'Gazipur'),
)

CITY_CHOICES = (
    ('cantonment-area', 'Cantonment Area'),
    ('abdullahpur', 'Abdullahpur'),
    ('uttara', 'Uttara'),
    ('mirpur', 'Mirpur'),
    ('pallabi', 'Pallabi'),
    ('kazipara', 'Kazipara'),
    ('kafrul', 'Kafrul'),
    ('agargaon', 'Agargaon'),
    ('sher-e-bangla', 'ShereBangla'),
    ('cantonment-area', 'Cantonment Area'),
    ('banani', 'Banani'),
    ('gulshan', 'Gulshan'),
    ('mohakhali', 'Mohakhali'),
    ('bashundhara', 'Bashundhara'),
    ('banasree', 'Banasree'),
    ('baridhara', 'Baridhara'),
    ('uttarkhan', 'Uttarkhan'),
    ('dakshinkhan', 'Dakshinkhan'),
    ('bawnia', 'Bawnia'),
    ('khilkhet', 'Khilkhet'),
    ('tejgaon', 'Tejgaon'),
    ('farmgate', 'Farmgate'),
    ('mohammadpur', 'Mohammadpur'),
    ('rampura', 'Rampura'),
    ('badda', 'Badda'),
    ('satarkul', 'Satarkul'),
    ('beraid', 'Beraid'),
    ('khilgaon', 'Khilgaon'),
    ('vatara', 'Vatara'),
    ('gabtali', 'Gabtali')
)

PRODUCT_STATUS = (
    ('normal', 'Normal'),
    ('lastest', 'Latest Product'),
    ('featured', 'Featured Product'),
    ('big_discount', 'Big Discount'),
    ('exclusive', 'Exclusive'),
)

PRODUCT_CATEGORY = (
    ('electronics', 'Electronics'),
    ('domestic', 'Domestic'),
)

ORDER_STATUS = (
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('packing', 'Packing Started'),
    ('packed', 'Packed'),
    ('on_the_way', 'On the way'),
    ('deliverd', 'Delivered')
)


PAY_CHOICES = (
    ('cod', 'Cash on delivery'),
    ('bkash', 'Bkash'),
    ('nagad', 'Nagad'),
)