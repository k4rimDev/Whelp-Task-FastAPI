from fastapi import HTTPException

from app.models.ip_address import IpAddress


def create_ip_address(response, user):
    ip_address = IpAddress(
        ip=response["ip"],
        user=user,
        is_eu=response["is_eu"],
        city=response["city"],
        region=response["region"],
        region_code=response["region_code"],
        country_name=response["country_name"],
        country_code=response["country_code"],
        continent_name=response["continent_name"],
        continent_code=response["continent_code"],
        latitude=response["latitude"],
        longitude=response["longitude"],
        postal=response["postal"],
        calling_code=response["calling_code"],
        flag=response["flag"]
    )
    ip_address.save()
    return ip_address


def get_status_of_task(ip_address_id):
    if ip_address := IpAddress.filter(IpAddress.id == ip_address_id).first():
        return ip_address
    return HTTPException(status_code=404, detail="IP Address not found")
