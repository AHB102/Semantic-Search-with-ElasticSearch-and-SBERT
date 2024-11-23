# ProductID             int64
# ProductName          object
# ProductBrand         object
# Gender               object
# Price (INR)           int64
# NumImages             int64
# Description          object
# PrimaryColor         object
# DescriptionVector    object

indexMapping = {
    "properties":{
        "ProductID":{
            "type":"long"
        },
        "ProductName":{
            "type":"text"

        },
        "ProductBrand":{
            "type":"text"

        },
        "Gender":{
            "type":"text"

        },
        "Price (INR)":{
            "type":"long"
        },
        "NumImages":{
            "type":"long"

        },
        "Description":{
            "type":"text"

        },
        "PrimaryColor":{
            "type":"text"

        },
        "DescriptionVector":{
            "type":"dense_vector",
            "dims": 768,
            "index":True,
            "similarity":"l2_norm"
        },

        "ProductNameVecor":{
            "type":"dense_vector",
            "dims": 768,
            "index":True,
            "similarity":"l2_norm"
        }
    }
}