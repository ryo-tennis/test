# 処理系のアルゴリズムを定義
class fuctionClass:

    def __init__(self):pass

    # update_dict(),update_list()でjsonの結合(参考；https://stackoverflow.com/questions/66383920/merge-deep-json-files-in-python)
    def update_dict(self, original, update):
        for key, value in update.items():

            # Add new key values
            if key not in original:
                original[key] = update[key]
                continue

            # Update the old key values with the new key values
            if key in original:
                if isinstance(value, dict):self.update_dict(original[key], update[key])
                if isinstance(value, list):self.update_list(original[key], update[key])
                if isinstance(value, (str, int, float)):original[key] = update[key]
        return original

    def update_list(self, original, update):
        # Make sure the order is equal, otherwise it is hard to compare the items.
        assert len(original) == len(update), "Can only handle equal length lists."

        for idx, (val_original, val_update) in enumerate(zip(original, update)):
            if not isinstance(val_original, type(val_update)):raise ValueError(f"Different types! {type(val_original)}, {type(val_update)}")
            if isinstance(val_original, dict):original[idx] = self.update_dict(original[idx], update[idx])
            if isinstance(val_original, (tuple, list)):original[idx] = self.update_list(original[idx], update[idx])
            if isinstance(val_original, (str, int, float)):original[idx] = val_update
        return original