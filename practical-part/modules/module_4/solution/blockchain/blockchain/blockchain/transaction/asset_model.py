class AssetModel:
    def __init__(self):

        self.asset_owners = {}

    def add_asset(self, isbn, owner_public_key):
        if isbn in self.asset_owners:
            return False
        self.asset_owners[isbn] = owner_public_key
        return True

    def get_asset_owner(self, isbn):
        return self.asset_owners.get(isbn, None)

    def update_asset_owner(self, isbn, new_owner_public_key):
        if isbn not in self.asset_owners:
            return False
        self.asset_owners[isbn] = new_owner_public_key
        return True
